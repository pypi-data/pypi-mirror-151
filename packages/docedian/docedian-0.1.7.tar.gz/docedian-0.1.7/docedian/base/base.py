Ambiente = {
    '1': '1 - Produccion',
    '2': '2 - Pruebas',
}


TipoDocumento = {
    '11': '11 - Registro civil',
    '12': '12 - Tarjeta de identidad',
    '13': '13 - Cédula de ciudadanía',
    '21': '21 - Tarjeta de extranjería',
    '22': '22 - Cédula de extranjería',
    '31': '31 - NIT',
    '41': '41 - Pasaporte',
    '42': '42 - Documento de identificación extranjero',
    '47': '47 - PEP',
    '50': '50 - NIT de otro país',
    '91': '91 - NUIP * ',
}


class Dianbase():

    @classmethod
    def compute_check_digit(cls, rut: str, identification_type: str) -> str:
        """
        @param rut(str): Rut without check digit
        @param identification_type(str): Identification type

        @return result(str): Return the check digit of the rut
        """
        result = 0
        if identification_type == '31':
            factor = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
            rut_ajustado=str(rut).rjust( 15, '0')
            total = sum(int(rut_ajustado[14-i]) * factor[i] for i in range(14)) % 11
            if total > 1:
                result =  11 - total
            else:
                result = total
        else:
            result = 0

        return result