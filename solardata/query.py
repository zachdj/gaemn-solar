""" Query builder for solarradiation database """

import solardata.sites as sites


class Query(object):
    def __init__(self, target_hour=1, site='griffin', start_date='2011-06-22', end_date='2012-04-30 23:45:00',
                 gaemn=True, window=False, rap_cell=False, rap_grid=False, nam_cell=False, nam_grid=False):
        self.target_hour = target_hour
        self.site = site
        self.site_id = sites.get_site_id_by_name(site)
        self.start_date = start_date
        self.end_date = end_date
        self.components = {
            'gaemn': gaemn,
            'window': window,
            'rap_cell': rap_cell,
            'rap_grid': rap_grid,
            'nam_cell': nam_cell,
            'nam_grid': nam_grid
        }

        h = target_hour

        # build the query with the selected components
        self.query = "SELECT sr.Day, sr.AdjDate "
        if gaemn:
            self.query += ",sr.AirTemp,sr.Humidity,sr.Dewpoint,sr.VaporP,sr.VaporPD,sr.BarometricP," \
                     "sr.WindSpeed,sr.WindDir, sr.SD,sr.MaxWind,sr.Pan,sr.SR,sr.TSR,sr.PAR,sr.Rain,sr.Rain2 "
        if window:
            self.query += ",psr1.sr AS psr1,psr2.sr AS psr2,psr3.sr AS psr3,psr4.sr AS psr4,psr5.sr AS psr5,psr6.sr AS psr6," \
                     "psr7.sr AS psr7,psr8.sr AS psr8,psr9.sr AS psr9,psr10.sr AS psr10,psr11.sr AS psr11,psr12.sr AS psr12," \
                     "psr13.sr AS psr13,psr14.sr AS psr14,psr15.sr AS psr15,psr16.sr AS psr16,psr17.sr AS psr17," \
                     "psr18.sr AS psr18,psr19.sr AS psr19,psr20.sr AS psr20,psr21.sr AS psr21,psr22.sr AS psr22," \
                     "psr23.sr AS psr23,psr24.sr AS psr24 "

        if rap_cell:
            self.query += ",gp_rap.Temperature AS RAPTemp, gp_rap.PrecipitationRate AS RAPPrecipRate, " \
                          "gp_rap.Visibility AS RAPVis, gp_rap.WindSpeed AS RAPWindSpeed, " \
                          "gp_rap.WindDirection AS RAPWidDir, gp_rap.DewPointTemperature AS RAPDewPoint, " \
                          "gp_rap.AirPressure AS RAPAirPressure, gp_rap.RelativeHumidity AS RAPRelativeHumidity "

        if rap_grid:
            self.query += ",gp_rap_West.Temperature AS RAPWestTemp,gp_rap_West.PrecipitationRate AS RAPWestPrecipRate,gp_rap_West.Visibility AS RAPWestVis," \
                          "gp_rap_West.WindSpeed AS RAPWestWindSpeed,gp_rap_West.WindDirection AS RAPWestWidDir," \
                          "gp_rap_West.DewPointTemperature AS RAPWestDewPoint,gp_rap_West.AirPressure AS RAPWestAirPressure," \
                          "gp_rap_West.RelativeHumidity AS RAPWestRelativeHumidity," \
                          "" \
                          "gp_rap_East.Temperature AS RAPEastTemp,gp_rap_East.PrecipitationRate AS RAPEastPrecipRate," \
                          "gp_rap_East.Visibility AS RAPEastVis, gp_rap_East.WindSpeed AS RAPEastWindSpeed," \
                          "gp_rap_East.WindDirection AS RAPEastWidDir,gp_rap_East.DewPointTemperature AS RAPEastDewPoint," \
                          "gp_rap_East.AirPressure AS RAPEastAirPressure,gp_rap_East.RelativeHumidity AS RAPEastRelativeHumidity," \
                          "" \
                          "gp_rap_North.Temperature AS RAPNorthTemp,gp_rap_North.PrecipitationRate AS RAPNorthPrecipRate," \
                          "gp_rap_North.Visibility AS RAPNorthVis,gp_rap_North.WindSpeed AS RAPNorthWindSpeed," \
                          "gp_rap_North.WindDirection AS RAPNorthWidDir,gp_rap_North.DewPointTemperature AS RAPNorthDewPoint," \
                          "gp_rap_North.AirPressure AS RAPNorthAirPressure,gp_rap_North.RelativeHumidity AS RAPNorthRelativeHumidity," \
                          "" \
                          "gp_rap_South.Temperature AS RAPSouthTemp,gp_rap_South.PrecipitationRate AS RAPSouthPrecipRate," \
                          "gp_rap_South.Visibility AS RAPSouthVis,gp_rap_South.WindSpeed AS RAPSouthWindSpeed," \
                          "gp_rap_South.WindDirection AS RAPSouthWidDir,gp_rap_South.DewPointTemperature AS RAPSouthDewPoint," \
                          "gp_rap_South.AirPressure AS RAPSouthAirPressure,gp_rap_South.RelativeHumidity AS RAPSouthRelativeHumidity," \
                          "" \
                          "gp_rap_Northwest.Temperature AS RAPNorthwestTemp,gp_rap_Northwest.PrecipitationRate AS RAPNorthwestPrecipRate," \
                          "gp_rap_Northwest.Visibility AS RAPNorthwestVis,gp_rap_Northwest.WindSpeed AS RAPNorthwestWindSpeed," \
                          "gp_rap_Northwest.WindDirection AS RAPNorthwestWidDir,gp_rap_Northwest.DewPointTemperature AS RAPNorthwestDewPoint," \
                          "gp_rap_Northwest.AirPressure AS RAPNorthwestAirPressure," \
                          "gp_rap_Northwest.RelativeHumidity AS RAPNorthwestRelativeHumidity," \
                          "gp_rap_Northeast.Temperature AS RAPNortheastTemp,gp_rap_Northeast.PrecipitationRate AS RAPNortheastPrecipRate," \
                          "gp_rap_Northeast.Visibility AS RAPNortheastVis,gp_rap_Northeast.WindSpeed AS RAPNortheastWindSpeed," \
                          "gp_rap_Northeast.WindDirection AS RAPNortheastWidDir,gp_rap_Northeast.DewPointTemperature AS RAPNortheastDewPoint," \
                          "gp_rap_Northeast.AirPressure AS RAPNortheastAirPressure,gp_rap_Northeast.RelativeHumidity AS RAPNortheastRelativeHumidity," \
                          "" \
                          "gp_rap_Southeast.Temperature AS RAPSoutheastTemp,gp_rap_Southeast.PrecipitationRate AS RAPSoutheastPrecipRate," \
                          "gp_rap_Southeast.Visibility AS RAPSoutheastVis,gp_rap_Southeast.WindSpeed AS RAPSoutheastWindSpeed," \
                          "gp_rap_Southeast.WindDirection AS RAPSoutheastWidDir,gp_rap_Southeast.DewPointTemperature AS RAPSoutheastDewPoint," \
                          "gp_rap_Southeast.AirPressure AS RAPSoutheastAirPressure,gp_rap_Southeast.RelativeHumidity AS RAPSoutheastRelativeHumidity," \
                          "" \
                          "gp_rap_Southwest.Temperature AS RAPSouthwestTemp,gp_rap_Southwest.PrecipitationRate AS RAPSouthwestPrecipRate," \
                          "gp_rap_Southwest.Visibility AS RAPSouthwestVis,gp_rap_Southwest.WindSpeed AS RAPSouthwestWindSpeed," \
                          "gp_rap_Southwest.WindDirection AS RAPSouthwestWidDir,gp_rap_Southwest.DewPointTemperature AS RAPSouthwestDewPoint," \
                          "gp_rap_Southwest.AirPressure AS RAPSouthwestAirPressure," \
                          "gp_rap_Southwest.RelativeHumidity AS RAPSouthwestRelativeHumidity "

        if nam_cell:
            self.query += ", gp_nam.Temperature AS NAMTemperature, gp_nam.CloudCover AS NAMCloudCover," \
                          "gp_nam.PrecipitationProbability AS NAMPrecipitationProbability," \
                          "gp_nam.WindSpeed AS NAMWindSpeed,gp_nam.WindDirection AS NAMWindDirection," \
                          "gp_nam.MaxTemperature AS NAMMaxTemp, gp_nam.MinTemperature AS NAMMinTemp," \
                          "gp_nam.DewPointTemperature AS NAMDewPointTemp "

        if nam_grid:
            self.query += ", gp_nam_West.Temperature AS NAMWestTemperature,gp_nam_West.CloudCover AS NAMWestCloudCover," \
                          "gp_nam_West.PrecipitationProbability AS NAMWestPrecipitationProbability," \
                          "gp_nam_West.WindSpeed AS NAMWestWindSpeed,gp_nam_West.WindDirection AS NAMWestWindDirection," \
                          "gp_nam_West.MaxTemperature AS NAMWestMaxTemp," \
                          "gp_nam_West.MinTemperature AS NAMWestMinTemp," \
                          "gp_nam_West.DewPointTemperature AS NAMWestDewPointTemp," \
                          "" \
                          "gp_nam_North.Temperature AS NAMNorthTemperature,gp_nam_North.CloudCover AS NAMNorthCloudCover," \
                          "gp_nam_North.PrecipitationProbability AS NAMNorthPrecipitationProbability," \
                          "gp_nam_North.WindSpeed AS NAMNorthWindSpeed,gp_nam_North.WindDirection AS NAMNorthWindDirection," \
                          "gp_nam_North.MaxTemperature AS NAMNorthMaxTemp,gp_nam_North.MinTemperature AS NAMNorthMinTemp," \
                          "gp_nam_North.DewPointTemperature AS NAMNorthDewPointTemp," \
                          "" \
                          "gp_nam_South.Temperature AS NAMSouthTemperature,gp_nam_South.CloudCover AS NAMSouthCloudCover," \
                          "gp_nam_South.PrecipitationProbability AS NAMSouthPrecipitationProbability," \
                          "gp_nam_South.WindSpeed AS NAMSouthWindSpeed,gp_nam_South.WindDirection AS NAMSouthWindDirection," \
                          "gp_nam_South.MaxTemperature AS NAMSouthMaxTemp,gp_nam_South.MinTemperature AS NAMSouthMinTemp," \
                          "gp_nam_South.DewPointTemperature AS NAMSouthDewPointTemp," \
                          "" \
                          "gp_nam_East.Temperature AS NAMEastTemperature,gp_nam_East.CloudCover AS NAMEastCloudCover," \
                          "gp_nam_East.PrecipitationProbability AS NAMEastPrecipitationProbability," \
                          "gp_nam_East.WindSpeed AS NAMEastWindSpeed,gp_nam_East.WindDirection AS NAMEastWindDirection," \
                          "gp_nam_East.MaxTemperature AS NAMEastMaxTemp,gp_nam_East.MinTemperature AS NAMEastMinTemp," \
                          "gp_nam_East.DewPointTemperature AS NAMEastDewPointTemp," \
                          "" \
                          "gp_nam_Northwest.Temperature AS NAMNorthwestTemperature," \
                          "gp_nam_Northwest.CloudCover AS NAMNorthwestCloudCover," \
                          "gp_nam_Northwest.PrecipitationProbability AS NAMNorthwestPrecipitationProbability," \
                          "gp_nam_Northwest.WindSpeed AS NAMNorthwestWindSpeed," \
                          "gp_nam_Northwest.WindDirection AS NAMNorthwestWindDirection," \
                          "gp_nam_Northwest.MaxTemperature AS NAMNorthwestMaxTemp," \
                          "gp_nam_Northwest.MinTemperature AS NAMNorthwestMinTemp," \
                          "gp_nam_Northwest.DewPointTemperature AS NAMNorthwestDewPointTemp," \
                          "" \
                          "gp_nam_Northeast.Temperature AS NAMNortheastTemperature," \
                          "gp_nam_Northeast.CloudCover AS NAMNortheastCloudCover," \
                          "gp_nam_Northeast.PrecipitationProbability AS NAMNortheastPrecipitationProbability," \
                          "gp_nam_Northeast.WindSpeed AS NAMNortheastWindSpeed," \
                          "gp_nam_Northeast.WindDirection AS NAMNortheastWindDirection," \
                          "gp_nam_Northeast.MaxTemperature AS NAMNortheastMaxTemp," \
                          "gp_nam_Northeast.MinTemperature AS NAMNortheastMinTemp," \
                          "gp_nam_Northeast.DewPointTemperature AS NAMNortheastDewPointTemp," \
                          "" \
                          "gp_nam_Southwest.Temperature AS NAMSouthWestTemperature," \
                          "gp_nam_Southwest.CloudCover AS NAMSouthWestCloudCover," \
                          "gp_nam_Southwest.PrecipitationProbability AS NAMSouthWestPrecipitationProbability," \
                          "gp_nam_Southwest.WindSpeed AS NAMSouthWestWindSpeed," \
                          "gp_nam_Southwest.WindDirection AS NAMSouthWestWindDirection," \
                          "gp_nam_Southwest.MaxTemperature AS NAMSouthWestMaxTemp," \
                          "gp_nam_Southwest.MinTemperature AS NAMSouthWestMinTemp," \
                          "gp_nam_Southwest.DewPointTemperature AS NAMSouthWestDewPointTemp," \
                          "" \
                          "gp_nam_Southeast.Temperature AS NAMSouthEastTemperature," \
                          "gp_nam_Southeast.CloudCover AS NAMSouthEastCloudCover," \
                          "gp_nam_Southeast.PrecipitationProbability AS NAMSouthEastPrecipitationProbability," \
                          "gp_nam_Southeast.WindSpeed AS NAMSouthEastWindSpeed," \
                          "gp_nam_Southeast.WindDirection AS NAMSouthEastWindDirection," \
                          "gp_nam_Southeast.MaxTemperature AS NAMSouthEastMaxTemp," \
                          "gp_nam_Southeast.MinTemperature AS NAMSouthEastMinTemp," \
                          "gp_nam_Southeast.DewPointTemperature AS NAMSouthEastDewPointTemp "

        # add target hour
        self.query += f', sr{h}.SR as SR{h} '

        # join up all necessary tables
        self.query += " from solarradiation sr "
        self.query += f' INNER JOIN solarradiation sr{h} ON sr{h}.id=sr.id+{h*4} and sr.SiteID=sr{h}.SiteID '

        if window:
            self.query += f' INNER JOIN solarradiation psr1 ON psr1.id=sr.id-4' \
                     f' INNER JOIN solarradiation psr2 ON psr2.id=sr.id-8' \
                     f' INNER JOIN solarradiation psr3 ON psr3.id=sr.id-12' \
                     f' INNER JOIN solarradiation psr4 ON psr4.id=sr.id-16' \
                     f' INNER JOIN solarradiation psr5 ON psr5.id=sr.id-20' \
                     f' INNER JOIN solarradiation psr6 ON psr6.id=sr.id-24' \
                     f' INNER JOIN solarradiation psr7 ON psr7.id=sr.id-28' \
                     f' INNER JOIN solarradiation psr8 ON psr8.id=sr.id-32' \
                     f' INNER JOIN solarradiation psr9 ON psr9.id=sr.id-36' \
                     f' INNER JOIN solarradiation psr10 ON psr10.id=sr.id-40' \
                     f' INNER JOIN solarradiation psr11 ON psr11.id=sr.id-44' \
                     f' INNER JOIN solarradiation psr12 ON psr12.id=sr.id-48' \
                     f' INNER JOIN solarradiation psr13 ON psr13.id=sr.id-52' \
                     f' INNER JOIN solarradiation psr14 ON psr14.id=sr.id-56' \
                     f' INNER JOIN solarradiation psr15 ON psr15.id=sr.id-60' \
                     f' INNER JOIN solarradiation psr16 ON psr16.id=sr.id-64' \
                     f' INNER JOIN solarradiation psr17 ON psr17.id=sr.id-68' \
                     f' INNER JOIN solarradiation psr18 ON psr18.id=sr.id-72' \
                     f' INNER JOIN solarradiation psr19 ON psr19.id=sr.id-76' \
                     f' INNER JOIN solarradiation psr20 ON psr20.id=sr.id-80' \
                     f' INNER JOIN solarradiation psr21 ON psr21.id=sr.id-84' \
                     f' INNER JOIN solarradiation psr22 ON psr22.id=sr.id-88' \
                     f' INNER JOIN solarradiation psr23 ON psr23.id=sr.id-92' \
                     f' INNER JOIN solarradiation psr24 ON psr24.id=sr.id-96 '

        if rap_cell:
            self.query += f' INNER JOIN gribprediction gp_rap ' \
                          f'ON gp_rap.SolarRadiationID=sr.id ' \
                          f'AND (gp_rap.Datasource="rap" OR gp_rap.Datasource="rapinterpolation") ' \
                          f'AND gp_rap.HoursAhead=1 AND gp_rap.cell="" and gp_rap.SiteID=sr.siteID '

        if rap_grid:
            self.query += " INNER JOIN gribprediction gp_rap_West ON gp_rap_West.SolarRadiationID=sr.id " \
                          "AND (gp_rap_West.Datasource='rap' OR gp_rap_West.Datasource='rapinterpolation') " \
                          "AND gp_rap_West.HoursAhead=1 AND gp_rap_West.cell='West' AND gp_rap.SiteID=gp_rap_West.SiteID " \
                          "INNER JOIN gribprediction gp_rap_East ON gp_rap_East.SolarRadiationID=sr.id " \
                          "AND (gp_rap_East.Datasource='rap' OR gp_rap_East.Datasource='rapinterpolation') " \
                          "AND gp_rap_East.HoursAhead=1 AND gp_rap_East.cell='East' AND gp_rap.SiteID=gp_rap_East.SiteID " \
                          "INNER JOIN gribprediction gp_rap_North ON gp_rap_North.SolarRadiationID=sr.id " \
                          "AND (gp_rap_North.Datasource='rap' OR gp_rap_North.Datasource='rapinterpolation') " \
                          "AND gp_rap_North.HoursAhead=1 AND gp_rap_North.cell='North' AND gp_rap.SiteID=gp_rap_North.SiteID " \
                          "INNER JOIN gribprediction gp_rap_South ON gp_rap_South.SolarRadiationID=sr.id " \
                          "AND (gp_rap_South.Datasource='rap' OR gp_rap_South.Datasource='rapinterpolation') " \
                          "AND gp_rap_South.HoursAhead=1 AND gp_rap_South.cell='South' AND gp_rap.SiteID=gp_rap_South.SiteID " \
                          "INNER JOIN gribprediction gp_rap_Northwest ON gp_rap_Northwest.SolarRadiationID=sr.id " \
                          "AND (gp_rap_Northwest.Datasource='rap' OR gp_rap_Northwest.Datasource='rapinterpolation') " \
                          "AND gp_rap_Northwest.HoursAhead=1 AND gp_rap_Northwest.cell='Northwest' " \
                          "AND gp_rap.SiteID=gp_rap_Northwest.SiteID " \
                          "INNER JOIN gribprediction gp_rap_Northeast ON gp_rap_Northeast.SolarRadiationID=sr.id " \
                          "AND (gp_rap_Northeast.Datasource='rap' OR gp_rap_Northeast.Datasource='rapinterpolation') " \
                          "AND gp_rap_Northeast.HoursAhead=1 AND gp_rap_Northeast.cell='Northeast' " \
                          "AND gp_rap.SiteID=gp_rap_Northeast.SiteID " \
                          "INNER JOIN gribprediction gp_rap_Southwest ON gp_rap_Southwest.SolarRadiationID=sr.id " \
                          "AND (gp_rap_Southwest.Datasource='rap' OR gp_rap_Southwest.Datasource='rapinterpolation') " \
                          "AND gp_rap_Southwest.HoursAhead=1 AND gp_rap_Southwest.cell='Southwest' " \
                          "AND gp_rap.SiteID=gp_rap_Southwest.SiteID " \
                          "INNER JOIN gribprediction gp_rap_Southeast ON gp_rap_Southeast.SolarRadiationID=sr.id " \
                          "AND (gp_rap_Southeast.Datasource='rap' OR gp_rap_Southeast.Datasource='rapinterpolation') " \
                          "AND gp_rap_Southeast.HoursAhead=1 AND gp_rap_Southeast.cell='Southeast' " \
                          "AND gp_rap.SiteID=gp_rap_Southeast.SiteID "

        if nam_cell:
            self.query += " INNER JOIN gribprediction gp_nam ON gp_nam.SolarRadiationID=sr.id " \
                          "AND (gp_nam.Datasource='NAM' OR gp_nam.Datasource='NAMInterpolation') " \
                          "AND gp_nam.HoursAhead=24 AND gp_nam.cell='' and gp_nam.SiteID=sr.siteID "
        if nam_grid:
            self.query += " INNER JOIN gribprediction gp_nam_West ON gp_nam_West.SolarRadiationID=sr.id " \
                          "AND (gp_nam_West.Datasource='NAM' OR gp_nam_West.Datasource='NAMInterpolation') " \
                          "AND gp_nam_West.HoursAhead=24 AND gp_nam_West.cell='West' AND gp_nam_West.SiteID=sr.siteID " \
                          "" \
                          "INNER JOIN gribprediction gp_nam_East ON gp_nam_East.SolarRadiationID=sr.id " \
                          "AND (gp_nam_East.Datasource='NAM' OR gp_nam_East.Datasource='NAMInterpolation') " \
                          "AND gp_nam_East.HoursAhead=24 AND gp_nam_East.cell='East' AND gp_nam_East.SiteID=sr.siteID " \
                          "" \
                          "INNER JOIN gribprediction gp_nam_North ON gp_nam_North.SolarRadiationID=sr.id " \
                          "AND (gp_nam_North.Datasource='NAM' OR gp_nam_North.Datasource='NAMInterpolation') " \
                          "AND gp_nam_North.HoursAhead=24 AND gp_nam_North.cell='North' AND gp_nam_North.SiteID=sr.siteID " \
                          "" \
                          "INNER JOIN gribprediction gp_nam_South ON gp_nam_South.SolarRadiationID=sr.id " \
                          "AND (gp_nam_South.Datasource='NAM' OR gp_nam_South.Datasource='NAMInterpolation') " \
                          "AND gp_nam_South.HoursAhead=24 AND gp_nam_South.cell='South' AND gp_nam_South.SiteID=sr.siteID " \
                          "" \
                          "INNER JOIN gribprediction gp_nam_Northwest ON gp_nam_Northwest.SolarRadiationID=sr.id " \
                          "AND (gp_nam_Northwest.Datasource='NAM' OR gp_nam_Northwest.Datasource='NAMInterpolation') " \
                          "AND gp_nam_Northwest.HoursAhead=24 AND gp_nam_Northwest.cell='Northwest' AND gp_nam_Northwest.SiteID=sr.siteID " \
                          "" \
                          "INNER JOIN gribprediction gp_nam_Northeast ON gp_nam_Northeast.SolarRadiationID=sr.id " \
                          "AND (gp_nam_Northeast.Datasource='NAM' OR gp_nam_Northeast.Datasource='NAMInterpolation') " \
                          "AND gp_nam_Northeast.HoursAhead=24 AND gp_nam_Northeast.cell='Northeast' " \
                          "AND gp_nam_Northeast.SiteID=sr.siteID " \
                          "" \
                          "INNER JOIN gribprediction gp_nam_Southwest ON gp_nam_Southwest.SolarRadiationID=sr.id " \
                          "AND (gp_nam_Southwest.Datasource='NAM' OR gp_nam_Southwest.Datasource='NAMInterpolation') " \
                          "AND gp_nam_Southwest.HoursAhead=24 AND gp_nam_Southwest.cell='Southwest' " \
                          "AND gp_nam_Southwest.SiteID=sr.siteID " \
                          "" \
                          "INNER JOIN gribprediction gp_nam_Southeast ON gp_nam_Southeast.SolarRadiationID=sr.id " \
                          "AND (gp_nam_Southeast.Datasource='NAM' OR gp_nam_Southeast.Datasource='NAMInterpolation') " \
                          "AND gp_nam_Southeast.HoursAhead=24 AND gp_nam_Southeast.cell='Southeast' " \
                          "AND gp_nam_Southeast.SiteID=sr.siteID "

        # add date, site, and size constraints
        self.query += f' WHERE sr.dateandtime BETWEEN "{start_date}" AND "{end_date}" ' \
                      f' AND sr.SiteID={self.site_id} ' \
                      f' ORDER BY sr.dateandtime LIMIT 500000;'

    def __str__(self):
        return self.query
