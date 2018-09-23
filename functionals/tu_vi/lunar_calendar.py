# -*- coding: utf-8 -*-
__author__ = 'sunary'


import datetime
import math


class LunarCalendar(object):
    """
    source: http://www.informatik.uni-leipzig.de/~duc/amlich
    """
    def __init__(self):
        self.thien_can = ['giáp', 'ất', 'bính', 'đinh', 'mậu', 'kỷ', 'canh', 'tân', 'nhâm', 'quý']
        self.dia_chi = ['tý', 'sữu', 'dần', 'mão', 'thìn', 'tỵ', 'ngọ', 'mùi', 'thân', 'dậu', 'tuất', 'hợi']

    def date_to_julius(self, date):
        a = (14 - date.month)/12
        y = date.year + 4800 - a
        m = date.month + 12*a - 3

        jd = date.day + (153*m + 2)/5 + 365*y + y/4 - y/100 + y/400 - 32045
        if jd < 2299161:
            jd = date.day + (153*m + 2)/5 + 365*y + y/4 - 32083

        return jd

    def julius_to_date(self, jd):
        if jd > 2299160:
            # After 5/10/1582, Gregorian calendar
            a = jd + 32044
            b = (4*a + 3)/146097
            c = a - (b*146097)/4
        else:
            b = 0
            c = jd + 32082

        d = (4*c + 3)/1461
        e = c - (1461*d)/4
        m = (5*e + 2)/153

        day = e - (153*m + 2)/5 + 1
        month = m + 3 - 12*(m/10)
        year = b*100 + d - 4800 + m/10

        return datetime.datetime(year, month, day)

    def newmoon(self, k):
        """
        Compute the time of the k-th new moon after the new moon of 1/1/1900 13:52 UCT
        (measured as the number of days since 1/1/4713 BC noon UCT,
            e.g., 2451545.125 is 1/1/2000 15:00 UTC. Returns a floating number,
            e.g., 2415079.9758617813 for k=2 or 2414961.935157746 for k=-2.)
        """
        T = k / 1236.85
        T2 = T * T
        T3 = T2 * T
        dr = math.pi / 180.
        Jd1 = 2415020.75933 + 29.53058868*k + 0.0001178*T2 - 0.000000155*T3
        Jd1 = Jd1 + 0.00033*math.sin((166.56 + 132.87*T - 0.009173*T2)*dr)
        # Mean new moon

        M = 359.2242 + 29.10535608*k - 0.0000333*T2 - 0.00000347*T3
        # Sun's mean anomaly

        Mpr = 306.0253 + 385.81691806*k + 0.0107306*T2 + 0.00001236*T3
        # Moon's mean anomaly

        F = 21.2964 + 390.67050646*k - 0.0016528*T2 - 0.00000239*T3
        # Moon's argument of latitude

        C1 = (0.1734 - 0.000393*T)*math.sin(M*dr) + 0.0021*math.sin(2*dr*M)
        C1 = C1 - 0.4068*math.sin(Mpr*dr) + 0.0161*math.sin(dr*2*Mpr)
        C1 = C1 - 0.0004*math.sin(dr*3*Mpr)
        C1 = C1 + 0.0104*math.sin(dr*2*F) - 0.0051*math.sin(dr*(M + Mpr))
        C1 = C1 - 0.0074*math.sin(dr*(M - Mpr)) + 0.0004*math.sin(dr*(2*F + M))
        C1 = C1 - 0.0004*math.sin(dr*(2*F - M)) - 0.0006*math.sin(dr*(2*F + Mpr))
        C1 = C1 + 0.0010*math.sin(dr*(2*F - Mpr)) + 0.0005*math.sin(dr*(2*Mpr + M))

        if T < -11:
            delta_t = 0.001 + 0.000839*T + 0.0002261*T2 - 0.00000845*T3 - 0.000000081*T*T3
        else:
            delta_t = -0.000278 + 0.000265*T + 0.000262*T2

        return Jd1 + C1 - delta_t

    def sun_longitude(self, jdn, time_zone):
        T = (jdn - 2451545) / 36525

        T2 = T * T
        dr = math.pi/180
        M = 357.52910 + 35999.05030*T - 0.0001559*T2 - 0.00000048*T*T2
        # mean anomaly, degree

        L0 = 280.46645 + 36000.76983*T + 0.0003032*T2
        # mean longitude, degree

        DL = (1.914600 - 0.004817*T - 0.000014*T2)*math.sin(dr*M)
        DL = DL + (0.019993 - 0.000101*T)*math.sin(dr*2*M) + 0.000290*math.sin(dr*3*M)
        L = L0 + DL # true longitude, degree

        omega = 125.04 - 1934.136 * T
        L = L - 0.00569 - 0.00478 * math.sin(omega * dr)
        L = L*dr
        L = L - math.pi*2*(self.int(L/(math.pi*2)))
        return L

    def get_sun_longitude(self, day_number, time_zone):
        """
        Compute sun position at midnight of the day with the given Julian day number.
        The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.
        The function returns a number between 0 and 11.
        From the day after March equinox and the 1st major term after March equinox, 0 is returned.
        After that, return 1, 2, 3 ...
        """

        return self.int(self.sun_longitude(day_number - 0.5 - time_zone/24, time_zone)/ math.pi*6)

    def get_newmoon_day(self, k, time_zone):
        '''
        Compute the day of the k-th new moon in the given time zone.
        The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.
        '''
        return self.int(self.newmoon(k) + 0.5 + time_zone / 24.)

    def get_lunar_month11(self, year, time_zone):
        """
        Find the day that starts the luner month 11of the given year for the given time zone.
        """

        off = self.date_to_julius(datetime.datetime(year, 12, 31)) - 2415021.
        k = self.int(off / 29.530588853)
        nm = self.get_newmoon_day(k, time_zone)
        sunLong = self.get_sun_longitude(nm, time_zone)
        # sun longitude at local midnight

        if sunLong >= 9:
            nm = self.get_newmoon_day(k - 1, time_zone)

        return nm

    def get_leapmonth_offset(self, a11, time_zone):
        '''
        Find the index of the leap month after the month starting on the day a11.
        '''
        k = self.int((a11 - 2415021.076998695)/ 29.530588853 + 0.5)
        last = 0
        i = 1  # start with month following lunar month 11
        arc = self.get_sun_longitude(self.get_newmoon_day(k + i, time_zone), time_zone)
        while True:
            last = arc
            i += 1
            arc = self.get_sun_longitude(self.get_newmoon_day(k + i, time_zone), time_zone)
            if not (arc != last and i < 14):
              break

        return i - 1

    def sun_to_lunar(self, date, time_zone=7.0):
        dayNumber = self.date_to_julius(date)
        k = self.int((dayNumber - 2415021.076998695)/ 29.530588853)
        monthStart = self.get_newmoon_day(k + 1, time_zone)

        if monthStart > dayNumber:
            monthStart = self.get_newmoon_day(k, time_zone)
        # alert(dayNumber + " -> " + monthStart)

        a11 = self.get_lunar_month11(date.year, time_zone)
        b11 = a11
        if a11 >= monthStart:
            lunarYear = date.year
            a11 = self.get_lunar_month11(date.year - 1, time_zone)
        else:
            lunarYear = date.year + 1
            b11 = self.get_lunar_month11(date.year + 1, time_zone)

        lunarDay = dayNumber - monthStart + 1
        diff = self.int((monthStart - a11) / 29.)
        lunarLeap = 0
        lunarMonth = diff + 11

        if b11 - a11 > 365:
            leapMonthDiff = self.get_leapmonth_offset(a11, time_zone)
            if diff >= leapMonthDiff:
                lunarMonth = diff + 10
                if diff == leapMonthDiff:
                    lunarLeap = 1

        if lunarMonth > 12:
            lunarMonth = lunarMonth - 12

        if lunarMonth >= 11 and diff < 4:
            lunarYear -= 1

        return datetime.datetime(lunarYear, lunarMonth, lunarDay), lunarLeap

    def lunar_to_sun(self, date, lunarLeap=0, time_zone=7.):
        if date.month < 11:
            a11 = self.get_lunar_month11(date.year - 1, time_zone)
            b11 = self.get_lunar_month11(date.year, time_zone)
        else:
            a11 = self.get_lunar_month11(date.year, time_zone)
            b11 = self.get_lunar_month11(date.year + 1, time_zone)

        k = self.int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
        off = date.month - 11
        if off < 0:
            off += 12
        if b11 - a11 > 365:
            leapOff = self.get_leapmonth_offset(a11, time_zone)
            leapM = leapOff - 2

            if leapM < 0:
                leapM += 12

            if lunarLeap != 0 and date.month != leapM:
                return None
            elif lunarLeap != 0 or off >= leapOff:
                off += 1

        monthStart = self.get_newmoon_day(k + off, time_zone)

        return self.julius_to_date(monthStart + date.day - 1)

    def day_of_week(self, date):
        week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        jd = self.date_to_julius(date)

        return week[(jd + 1) % 7]

    def can_chi_name(self, date, lunarLeap):
        can_year = (date.year + 6) % 10
        chi_year = (date.year + 8) % 12

        jd = self.date_to_julius(self.lunar_to_sun(date, lunarLeap))
        can_day = (jd + 9) % 10
        chi_day = (jd + 1) % 12

        can_month = (date.year * 12 + date.month + 3) % 10
        chi_month = (date.month + 1) % 12

        return 'ngày {0} ({1}), tháng {2} ({3}){4}, năm {5}'\
            .format(date.day, self.thien_can[can_day] + ' ' + self.dia_chi[chi_day],
                    date.month, self.thien_can[can_month] + ' ' + self.dia_chi[chi_month],
                    ' - nhuận' if lunarLeap else '', self.thien_can[can_year] + ' ' + self.dia_chi[chi_year])

    def hour_to_can_chi(self, hour):
        return self.dia_chi[((hour + 1)/2) % 12]

    def int(self, x):
        return int(math.floor(x))


if __name__ == '__main__':
    vn_lunar = LunarCalendar()
    print(vn_lunar.sun_to_lunar(datetime.datetime(1974, 2, 5)))
    print(vn_lunar.day_of_week(datetime.datetime.now()))
    print(vn_lunar.day_of_week(datetime.datetime(1991, 2, 5)))

    lunar_date = vn_lunar.sun_to_lunar(datetime.datetime.now())
    print(vn_lunar.can_chi_name(lunar_date[0], lunar_date[1]))

    lunar_date = vn_lunar.sun_to_lunar(datetime.datetime(2015, 12, 27))
    print(vn_lunar.can_chi_name(lunar_date[0], lunar_date[1]))
    print(vn_lunar.lunar_to_sun(datetime.datetime(2015, 11, 17), 0))

    print(vn_lunar.hour_to_can_chi(11))
