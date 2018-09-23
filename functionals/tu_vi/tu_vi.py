# -*- coding: utf-8 -*-
__author__ = 'sunary'


from lunar_calendar import LunarCalendar
from datetime import datetime


THIEN_CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
DIA_CHI = ['Tý', 'Sữu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
CUNG = ['Mệnh', 'Phụ Mẫu', 'Phúc Đức', 'Điền Trạch', 'Quan Lộc', 'Nô Bộc',
        'Thiên Di', 'Tạch Ách', 'Tài Bạch', 'Tử Nữ', 'Phu Thê', 'Huynh Đệ']
CUNG_THAN = ['Mệnh', 'Phúc Đức', 'Quan Lộc', 'Thiên Di', 'Tài Bạch', 'Phu Thê']
CUC_NGUHANH = ['Thủy nhị cục', 'Mộc tam cục', 'Kim tứ cục', 'Thổ ngũ cục', 'Hỏa lục cục']
CUNG_PHI = ['Ly', 'Khảm', 'Khôn', 'Chấn', 'Tốn', ['Khôn', 'Cấn'], 'Càn', 'Đoài', 'Cấn']
NGUHANH_NAPAM = {
    'Hải Trung Kim': (((0, 0), (1, 1)), 0),
    'Kiếm Phong Kim': (((8, 8), (9, 9)), 0),
    'Bạch Lạp Kim': (((6, 4), (7, 5)), 0),
    'Tích Lịch Hỏa': (((4, 0), (5, 1)), 3),
    'Sơn Hạ Hỏa': (((2, 8), (3, 9)), 3),
    'Phú Đăng Hỏa': (((0, 4), (1, 5)), 3),
    'Tăng Đố Mộc': (((8, 0), (9, 1)), 1),
    'Thạch Lựu Mộc': (((6, 8), (7, 9)), 1),
    'Ðại Lâm Mộc': (((4, 4), (5, 5)), 1),
    'Giang Hạ Thủy': (((2, 0), (3, 1)), 2),
    'Tuyền Trung Thủy': (((0, 8), (1, 9)), 2),
    'Trường Lưu Thủy': (((8, 4), (9, 5)), 2),
    'Bích Thuợng Thổ': (((6, 0), (7, 1)), 4),
    'Đại Dịch Thổ': (((4, 8), (5, 9)), 4),
    'Sa Trung Thổ': (((2, 4), (3, 5)), 4),
    'Sa Trung Kim': (((0, 6), (1, 7)), 0),
    'Kim Bạch Kim': (((8, 2), (9, 3)), 0),
    'Thoa Xuyến Kim': (((6, 10), (7, 11)), 0),
    'Thiên Thuợng Hỏa': (((4, 6), (5, 7)), 3),
    'Lư Trung Hỏa': (((2, 2), (3, 3)), 3),
    'Sơn Đầu Hỏa': (((0, 10), (1, 11)), 3),
    'Dương Liễu Mộc': (((8, 6), (9, 7)), 1),
    'Tùng Bá Mộc': (((6, 2), (7, 3)), 1),
    'Bình Địa Mộc': (((4, 10), (5, 11)), 1),
    'Thiên Hà Thủy': (((2, 6), (3, 7)), 2),
    'Ðại Khe Thủy': (((0, 2), (1, 3)), 2),
    'Ðại Hải Thủy': (((8, 10), (9, 11)), 2),
    'Lộ Bàng Thổ': (((6, 6), (7, 7)), 4),
    'Thành Đầu Thổ': (((4, 2), (5, 3)), 4),
    'Ốc Thuợng Thổ': (((2, 10), (3, 11)), 4)
}
MENH_CHU = ['Tham lang', ' Cự môn', 'Lộc tồn', 'Văn khúc', 'Vũ khúc', 'Liêm trinh', 'Phá quân']
THAN_CHU = ['Hỏa tinh', 'Thiên tướng', 'Thiên lương', 'Thiên đồng', 'Văn xương', 'Thiên cơ']
SAO_HAN = ['La Hầu', 'Thổ Tú', 'Thủy Diệu', 'Thái Bạch', 'Thái Dương', 'Vân Hớn', 'Kế Đô', 'Thái Âm', 'Mộc Đức']
SAO_HAN_NAM_INDEX = [0, 1, 2, 3, 4, 5, 6, 7, 8]
SAO_HAN_NU_INDEX = [6, 5, 8, 7, 1, 0, 4, 3, 2]


class BirthDay(object):

    def __init__(self, y, m, d, h=0, leaf_month=False):
        self.year = y
        self.month = m
        self.day = d
        self.hour = h
        self.leaf_month = leaf_month


class TuVi(object):

    def __init__(self):
        self.lunar_calendar = LunarCalendar()

    def input_am_lich(self, am_lich, gioitinh_nam):
        self.am_lich = am_lich
        duong_lich = self.lunar_calendar.lunar_to_sun(
            datetime(am_lich.day, am_lich.month, am_lich.year), int(am_lich.leaf_month))
        self.duong_lich = BirthDay(duong_lich[0], duong_lich[1], duong_lich[2], am_lich.hour)

        self.gioitinh_nam = gioitinh_nam

    def input_duong_lich(self, duong_lich, gioitinh_nam):
        self.duong_lich = duong_lich
        self.am_lich = self.sun_to_lunar(duong_lich)

        self.gioitinh_nam = gioitinh_nam

    def sun_to_lunar(self, duong_lich):
        am_lich = self.lunar_calendar.sun_to_lunar(datetime(duong_lich.year, duong_lich.month, duong_lich.day))
        if am_lich[1] and am_lich[0].day > 15:
            return BirthDay(am_lich[0].year, am_lich[0].month + 1, am_lich[0].day, duong_lich.hour)
        else:
            return BirthDay(am_lich[0].year, am_lich[0].month, am_lich[0].day, duong_lich.hour)

    def xem_tu_vi(self):
        can_birthday, chi_birthday = self.canchi_birthday(self.am_lich, self.duong_lich)

        print 'Lá số tử vi'
        print 'Sao hạn năm: {}'.format(self.tinh_saohan(self.am_lich)[0])
        print self.am_duong(can_birthday)

        canchi_start = self.canchi_laso(chi_birthday)
        print 'Bắt đầu lá số: {} {}'.format(THIEN_CAN[canchi_start[0]], DIA_CHI[canchi_start[1]])
        menh_than = self.tinh_menh_than(self.am_lich, chi_birthday)
        print 'An mệnh: ' + DIA_CHI[menh_than[0]] + ', An thân: ' + DIA_CHI[menh_than[1]]
        print self.quanhe_menhthan(chi_birthday, menh_than)
        print self.tinh_cungthan(chi_birthday)
        print self.tinh_cungphi(self.am_lich)[0]

        so_cuc = self.tinh_cuc((menh_than[0] - canchi_start[1] + canchi_start[0]) % 10, menh_than[0])
        menh_nguhanh = self.tinh_menhnguhanh(can_birthday, chi_birthday)
        print so_cuc[1]
        print menh_nguhanh[1]
        print self.menh_vs_cuc(menh_nguhanh[0], so_cuc[0])

        print 'Sao tử vi tại: ' + DIA_CHI[self.sao_tuvi(self.am_lich, so_cuc[0])]
        print self.sao_menhchu(chi_birthday)
        print self.sao_thanchu(chi_birthday)

    def canchi_birthday(self, am_lich, duong_lich):
        can_year = (am_lich.year + 6) % 10
        chi_year = (am_lich.year + 8) % 12

        can_month = (am_lich.year * 12 + am_lich.month + 3) % 10
        chi_month = (am_lich.month + 1) % 12

        jd = self.lunar_calendar.date_to_julius(duong_lich)
        can_day = (jd + 9) % 10
        chi_day = (jd + 1) % 12

        chi_hour = ((am_lich.hour + 1)/2) % 12
        can_hour = (chi_hour + (can_day % 5)*2) % 10

        return BirthDay(can_year, can_month, can_day, can_hour), BirthDay(chi_year, chi_month, chi_day, chi_hour)

    def tinh_saohan(self, am_lich):
        today_lunar = self.lunar_calendar.sun_to_lunar(datetime.now())[0]
        age = today_lunar.year - am_lich.year + 1
        if self.gioitinh_nam:
            return SAO_HAN[SAO_HAN_NAM_INDEX[(age - 10) % len(SAO_HAN)]], age
        else:
            return SAO_HAN[SAO_HAN_NU_INDEX[(age - 10) % len(SAO_HAN)]], age

    def am_duong(self, can_birthday):
        ret = 'Dương' if can_birthday.year % 2 == 0 else 'Âm'
        ret += ' Nam' if self.gioitinh_nam else ' Nữ'
        return ret

    def tinh_menh_than(self, am_lich, chi_birthday):
        table = ((2, 2), (1, 3), (0, 4), (11, 5), (10, 6), (9, 7), (8, 8), (9, 7), (6, 0), (5, 11), (4, 5), (3, 1))
        return (table[chi_birthday.hour][0] + am_lich.month - 1) % 12, \
               (table[chi_birthday.hour][1] + am_lich.month - 1) % 12

    def tinh_cungphi(self, am_lich):
        index = am_lich.year % 9
        if self.gioitinh_nam:
            index = 11 - index
        else:
            index += 4

        index %= 9
        group = 'Đông trạch' if index in (0, 1, 3, 4) else 'Tây trạch'

        if index == 5:
            return 'Cung phi: ' + CUNG_PHI[5][0 if self.gioitinh_nam else 1], group
        else:
            return 'Cung phi: ' + CUNG_PHI[index], group

    def tinh_cuc(self, can_menhcung, chi_menhcung):
        chi1 = (0, 1, 6, 7)
        chi2 = (2, 3, 8, 9)
        chi3 = (4, 5, 10, 11)
        table = [[((0, 1), chi2), ((2, 3), chi1), ((8, 9), chi3)],
                 [((4, 5), chi3), ((6, 7), chi2), ((8, 9), chi1)],
                 [((0, 1), chi1), ((6, 7), chi3), ((8, 9), chi2)],
                 [((2, 3), chi3), ((4, 5), chi2), ((6, 7), chi1)],
                 [((0, 1), chi3), ((2, 3), chi2), ((4, 5), chi1)]]

        for i, value in enumerate(table):
            for v in value:
                if can_menhcung in v[0] and chi_menhcung in v[1]:
                    return i, 'Cục ' + CUC_NGUHANH[i]

    def tinh_menhnguhanh(self, can_birthday, chi_birthday):
        for k, v in NGUHANH_NAPAM.items():
            if (can_birthday.year, chi_birthday.year) in v[0]:
                return v[1], 'Mệnh ' + k

    def menh_vs_cuc(self, menh_nguhanh, cuc_nguhanh):
        sinh_nguhanh = [(1, 4), (3, 4), (4, 2), (0, 0), (2, 1)]
        khac_nguhanh = [(1, 3), (4, 0), (2, 4), (3, 2), (0, 1)]

        if (menh_nguhanh, cuc_nguhanh) in sinh_nguhanh:
            return 'Mệnh sinh cục'
        elif (cuc_nguhanh, menh_nguhanh) in sinh_nguhanh:
            return 'Cục sinh mệnh'
        elif (menh_nguhanh, cuc_nguhanh) in khac_nguhanh:
            return 'Mệnh khắc cục'
        elif (cuc_nguhanh, menh_nguhanh) in khac_nguhanh:
            return 'Cục khắc mệnh'
        else:
            return 'Mệnh cục tị hòa'

    def tinh_cungthan(self, chi_birthday):
        table = [(0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11)]
        for i, value in enumerate(table):
            if chi_birthday.hour in value:
                return 'Thân cư ' + CUNG_THAN[i]

    def quanhe_menhthan(self, chi_birthday, menhthan):
        return 'Âm dương thuận lý' if (menhthan[0] % 2 == chi_birthday.year % 2) else 'Âm dương nghịch lý'

    def canchi_laso(self, chi_birthday):
        table = (2, 4, 6, 8, 0)

        can_start = table[chi_birthday.year % 5]
        chi_start = 2

        return can_start, chi_start

    def sao_tuvi(self, am_lich, so_cuc):
        so_cuc += 2
        if am_lich.day % so_cuc == 0:
            return (am_lich.day/so_cuc + 1) % 12
        else:
            mauso = so_cuc - am_lich.day % so_cuc
            if mauso % 2 == 0:
                return (am_lich.day/so_cuc + 1 + mauso + 1) % 12
            else:
                return (am_lich.day/so_cuc + 1 - mauso + 1) % 12

    def sao_menhchu(self, chi_birthday):
        table = [(0,), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11), (6,)]

        for i, v in enumerate(table):
            if chi_birthday.day in v:
                return 'Mệnh chủ ' + MENH_CHU[i]

    def sao_thanchu(self, chi_birthday):
        return 'Thân chủ ' + THAN_CHU[chi_birthday.day % 6]

    def tamphuong_tuchinh(self, cungmenh):
        return cungmenh, (cungmenh + 4) % 12, (cungmenh - 4) % 12, (cungmenh + 6) % 12


if __name__ == '__main__':
    birthday = BirthDay(1991, 2, 5, 16, False)
    tuvi = TuVi()
    tuvi.input_duong_lich(birthday, True)
    tuvi.xem_tu_vi()
