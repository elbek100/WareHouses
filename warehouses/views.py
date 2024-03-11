from typing import List

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from warehouses.models import Product, ProductMaterials, WareHouses, Numerator, Materials


# API - ()
class ProductMaterialsAPIView(APIView):
    permission_classes = ()

    """
        uz - POST metod. Bu metod product ID va miqdori bilan mahsulotlar ishlab chiqarish uchun xomashyolarni topadi
        ru - Метод POST. Этот метод находит склады для производства продуктов
    """

    def post(self, request):

        # POST so'rovi ma'lumotlarini dict ko'rinishida olish
        # Получить данные POST запроса в виде dict
        product_request = dict(request.data)

        result = []

        # product_id va quantity ma'lumotlarini ajratib olish
        # Извлечь данные product_id и quantity.
        product_ids = product_request.get('product_id', [])
        quantities = product_request.get('quantity', [])
        print(product_ids, quantities)

        # ma'lumotlarini tekshirish
        # проверить данные
        if not product_ids or not quantities or len(product_ids) != len(quantities):
            return Response({'message': 'Product ID or quantity is missing.'}, status=400)

        #
        for product_id, quantity in zip(product_ids, quantities):
            try:

                # Mahsulotni tekshirish bormi yoqmi
                # Проверка продукции есть или нет
                product = Product.objects.get(pk=product_id)

                # Mahsulotni ishlab chiqarish uchun xomashyolarni olish
                # Получение материалов для производства продукта
                product_materials = ProductMaterials.objects.filter(product_id=product.id)
            except Product.DoesNotExist:
                return Response({'message': f'Product with id {product_id} does not exist.'}, status=404)
            except ProductMaterials.DoesNotExist:
                return Response({'message': f'ProductMaterials with id {product_id} does not exist.'}, status=404)

            # Quantity ni tekshirish
            # Проверить quantity
            if quantity is None:
                return Response({'message': 'Quantity must be provided.'}, status=400)

            # Bo'sh ro'yxat yaratish
            # Создать пустой список
            product_materials_list = []

            # Har bir mahsulot materiali uchun ishlovchi tsikl
            # Рабочий цикл для каждого материала изделия
            for material in product_materials:

                # Talab qilingan mahsulot miqdori
                # Необходимое количество продукта
                count_needed = material.quantity * float(quantity)

                # Omborxonadan materialarni olish
                # Получить материалы со склада
                warehouses = WareHouses.objects.filter(material_id_id=material.material_id)
                num = 0

                # Omborxonadagi har bir mahsulot uchun
                # За каждый товар на складе
                for warehouse in warehouses:
                    try:

                        # Hisoblagichni topish
                        # Найти счетчик
                        numerator = Numerator.objects.get(warehouse=warehouse)

                        # Omborxonadagi qoldiq miqdorini hisoblash
                        # Расчет остатков на складе
                        if warehouse.remainder <= numerator.quantity:
                            continue

                        quantity_warehouse = warehouse.remainder - numerator.quantity

                        num += quantity_warehouse
                        if quantity_warehouse <= 0:
                            break

                        # Talab qilingan miqdor bilan omborxonadagi miqdorni solishtirish
                        # Сравнить запрошенное количество с количеством на складе.
                        qty_to_use = min(count_needed, quantity_warehouse)

                        # Hisoblagichni yangilash
                        # Обновить счетчик
                        numerator.quantity += qty_to_use
                        numerator.save()

                    except Numerator.DoesNotExist:
                        qty_to_use = min(count_needed, warehouse.remainder)
                        num += warehouse.remainder

                        # Yangi hisoblagich yaratish
                        # Создать новый счетчик
                        Numerator.objects.create(warehouse=warehouse, quantity=qty_to_use)

                    # Mahsulot materiali uchun ma'lumotlar ro'yxatiga qo'shish
                    # Добавить в список данных для материала продукта
                    product_materials_list.append({
                        'warehouse_id': warehouse.id,
                        'material_name': material.material.name,
                        'qty': qty_to_use,
                        'price': warehouse.price
                    })

                    count_needed -= qty_to_use

                    if count_needed <= 0:
                        break

                # Agar talab qilingan miqdor omborxonadagi miqdordan ko'p bo'lsa
                # Если запрошенное количество превышает количество на складе
                if (material.quantity * float(quantity)) > num:
                    product_materials_list.append({
                        'warehouse_id': None,
                        'material_name': material.material.name,
                        'qty': (material.quantity * float(quantity)) - num,
                        'price': None
                    })

            # Natijalarni asosiy ro'yxatga qo'shish
            # Добавление результатов в основной список
            result.append({
                'product_name': product.name,
                'quantity': float(quantity),
                'product_materials': product_materials_list
            })

        # Natijani qaytarish
        # Вернуть результат
        return Response({'result': result}, status=200)
