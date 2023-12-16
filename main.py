from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api
from models import Handphone as HandphoneModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from tabulate import tabulate

session = Session(engine)

app = Flask(__name__)
api = Api(app)


class BaseMethod():

    def __init__(self):
        self.raw_weight = {'ram_Gb': 4, 'rom_Gb': 4, 'chipset': 5, 'layar': 3, 'harga_Rp': 5, 'baterai_mAh': 4}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(HandphoneModel.id, HandphoneModel.nama_handphone, HandphoneModel.ram_Gb, HandphoneModel.rom_Gb, HandphoneModel.chipset,
                       HandphoneModel.layar, HandphoneModel.harga_Rp, HandphoneModel.baterai_mAh)
        result = session.execute(query).fetchall()
        print(result)
        return [{'id': Handphone.id, 'nama_handphone': Handphone.nama_handphone, 'ram_Gb': Handphone.ram_Gb, 'rom_Gb': Handphone.rom_Gb,
                'chipset': Handphone.chipset, 'layar': Handphone.layar, 'harga_Rp': Handphone.harga_Rp, 'baterai_mAh': Handphone.baterai_mAh} for Handphone in result]

    @property
    def normalized_data(self):
        ram_Gb_values = []  # max
        rom_Gb_values = []  # max
        chipset_values = []  # max
        layar_values = []  # max
        harga_Rp_values = []  # max
        baterai_mAh_values = []  # min

        for data in self.data:
            #RAM
            ram_Gb_values.append(int(data['ram_Gb']))
            
            #ROM
            rom_Gb_values.append(int(data['rom_Gb']))
            
            # chipset
            chipset_spec = data['chipset']
            chipset_numeric_values = [
                int(value) for value in chipset_spec.split() if value.isdigit()]
            max_chipset_value = max(
                chipset_numeric_values) if chipset_numeric_values else 1
            chipset_values.append(max_chipset_value)
            
            #Layar
            layar_spec = data['layar']
            layar_numeric_values = [float(value.split()[0]) for value in layar_spec.split(
            ) if value.replace('.', '').isdigit()]
            max_layar_value = max(
                layar_numeric_values) if layar_numeric_values else 1
            layar_values.append(max_layar_value)

            #Harga
            harga_Rp_values.append(int(data['harga_Rp']))

            #Baterai
            baterai_mAh_values.append(int(data['baterai_mAh']))

        return [
            {
                'id': data['id'],
                'nama_handphone': data['nama_handphone'],
                'ram_Gb': int(data['ram_Gb']) / max(ram_Gb_values) if max(ram_Gb_values) != 0 else 0,
                'rom_Gb': int(data['rom_Gb']) / max(rom_Gb_values) if max(rom_Gb_values) != 0 else 0,
                'chipset': chipset_value / max(chipset_values),
                'layar': layar_value / max(layar_values),
                'harga_Rp': int(data['harga_Rp']) / max(harga_Rp_values) if max(harga_Rp_values) != 0 else 0,
                'baterai_mAh': int(data['baterai_mAh']) / min(baterai_mAh_values) if min(baterai_mAh_values) != 0 else 0
            }
            for data,layar_value, chipset_value 
            in zip(self.data, layar_values, chipset_values)
        ]
    
    def update_weights(self, new_weights):
        self.raw_weight = new_weights


class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = [
            {
                'id': row['id'],
                'nama_handphone': row['nama_handphone'],
                'produk': 
                    row['ram_Gb'] ** self.weight['ram_Gb'] *
                    row['rom_Gb'] ** self.weight['rom_Gb'] *
                    row['chipset'] ** self.weight['chipset'] *
                    row['layar'] ** self.weight['layar'] *
                    row['harga_Rp'] ** self.weight['harga_Rp'] *
                    row['baterai_mAh'] ** self.weight['baterai_mAh']
            }
            for row in normalized_data
        ]
        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)
        sorted_data = [
            {
                'ID': product['id'],
                'nama_handphone': product['nama_handphone'],
                'score': round(product['produk'], 3)
            }
            for product in sorted_produk
        ]
        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return sorted(result, key=lambda x: x['score'], reverse=True), HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'handphone': sorted(result, key=lambda x: x['score'], reverse=True)}, HTTPStatus.OK.value


class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = [
            {
                'ID': row['id'],
                'nama_handphone': row['nama_handphone'],
                'Score': round(row['ram_Gb'] * weight['ram_Gb'] +
                                row['rom_Gb'] * weight['rom_Gb'] +
                                row['chipset'] * weight['chipset'] +
                                row['layar'] * weight['layar'] +
                                row['harga_Rp'] * weight['harga_Rp'] +
                                row['baterai_mAh'] * weight['baterai_mAh'], 3)
            }
            for row in self.normalized_data
        ]
        sorted_result = sorted(result, key=lambda x: x['Score'], reverse=True)
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights


class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return sorted(result, key=lambda x: x['Score'], reverse=True), HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'handphone': sorted(result, key=lambda x: x['Score'], reverse=True)}, HTTPStatus.OK.value


class Handphone(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None

        if page > page_count or page < 1:
            abort(404, description=f'Data Tidak Ditemukan.')
        return {
            'page': page,
            'page_size': page_size,
            'next': next_page,
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = session.query(HandphoneModel).order_by(HandphoneModel.id)
        result_set = query.all()
        data = [{'id': row.id, 'nama_handphone': row.nama_handphone, 'ram_Gb': row.ram_Gb, 'rom_Gb': row.rom_Gb,
                'chipset': row.chipset, 'layar': row.layar, 'harga_Rp': row.harga_Rp, 'baterai_mAh': row.baterai_mAh}
                for row in result_set]
        return self.get_paginated_result('xiaomi/', data, request.args), 200


api.add_resource(Handphone, '/hp')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)