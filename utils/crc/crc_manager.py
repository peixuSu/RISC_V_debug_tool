class CRC():
    # 自定义CRC-16算法
    def crc_16_user(data):
        crc = 0xFFFF
        poly = 0x8005

        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ poly
                else:
                    crc = crc << 1
                crc &= 0xFFFF

        return crc