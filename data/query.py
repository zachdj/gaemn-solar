"""
Query builder for solarradiation database
"""

def build(target_hour=1, site_id=115, gaemn=True, window=False, nam_cell=False, nam_grid=False,
                        start_date='2011-06-22', end_date='2012-04-30 23:45:00'):

    h = target_hour
    # build the selected attributes
    query = "SELECT sr.Day, sr.AdjDate "
    if gaemn:
        query += ",sr.AirTemp,sr.Humidity,sr.Dewpoint,sr.VaporP,sr.VaporPD,sr.BarometricP," \
                 "sr.WindSpeed,sr.WindDir, sr.SD,sr.MaxWind,sr.Pan,sr.SR,sr.TSR,sr.PAR,sr.Rain,sr.Rain2 "
    if window:
        query += ",psr1.sr AS psr1,psr2.sr AS psr2,psr3.sr AS psr3,psr4.sr AS psr4,psr5.sr AS psr5,psr6.sr AS psr6," \
                 "psr7.sr AS psr7,psr8.sr AS psr8,psr9.sr AS psr9,psr10.sr AS psr10,psr11.sr AS psr11,psr12.sr AS psr12," \
                 "psr13.sr AS psr13,psr14.sr AS psr14,psr15.sr AS psr15,psr16.sr AS psr16,psr17.sr AS psr17," \
                 "psr18.sr AS psr18,psr19.sr AS psr19,psr20.sr AS psr20,psr21.sr AS psr21,psr22.sr AS psr22," \
                 "psr23.sr AS psr23,psr24.sr AS psr24 "
    if nam_cell:
        query += ",gp.Temperature AS NamTemp,gp.PrecipitationRate AS NamPrecipRate,gp.Visibility AS NamVisibility," \
                 "gp.WindSpeed AS NamWindSpeed,gp.WindDirection AS NamWindDir," \
                 "gp.DewPointTemperature AS NamDewPointTemp,gp.AirPressure AS NamAirPressure,gp.RelativeHumidity AS NamHumidity "
    if nam_grid:
        query += (
            ",gpWest.Temperature AS CellWestTemp,gpWest.PrecipitationRate AS CellWestPrecipRate,gpWest.Visibility AS CellWestVis,"
            "gpWest.WindSpeed AS CellWestWindSpeed,gpWest.WindDirection AS CellWestWidDir,"
            "gpWest.DewPointTemperature AS CellWestDewPoint,gpWest.AirPressure AS CellWestAirPressure,gpWest.RelativeHumidity AS CellWestRelativeHumidity,"
            "gpEast.Temperature AS CellEastTemp,gpEast.PrecipitationRate AS CellEastPrecipRate,gpEast.Visibility AS CellEastVis,"
            "gpEast.WindSpeed AS CellEastWindSpeed,gpEast.WindDirection AS CellEastWidDir,"
            "gpEast.DewPointTemperature AS CellEastDewPoint,gpEast.AirPressure AS CellEastAirPressure,gpEast.RelativeHumidity AS CellEastRelativeHumidity,"
            "gpNorth.Temperature AS CellNorthTemp,gpNorth.PrecipitationRate AS CellNorthPrecipRate,gpNorth.Visibility AS CellNorthVis,"
            "gpNorth.WindSpeed AS CellNorthWindSpeed,gpNorth.WindDirection AS CellNorthWidDir,"
            "gpNorth.DewPointTemperature AS CellNorthDewPoint,gpNorth.AirPressure AS CellNorthAirPressure,gpNorth.RelativeHumidity AS CellNorthRelativeHumidity,"
            "gpSouth.Temperature AS CellSouthTemp,gpSouth.PrecipitationRate AS CellSouthPrecipRate,gpSouth.Visibility AS CellSouthVis,"
            "gpSouth.WindSpeed AS CellSouthWindSpeed,gpSouth.WindDirection AS CellSouthWidDir,"
            "gpSouth.DewPointTemperature AS CellSouthDewPoint,gpSouth.AirPressure AS CellSouthAirPressure,gpSouth.RelativeHumidity AS CellSouthRelativeHumidity,"
            "gpNorthwest.Temperature AS CellNorthwestTemp,gpNorthwest.PrecipitationRate AS CellNorthwestPrecipRate,gpNorthwest.Visibility AS CellNorthwestVis,"
            "gpNorthwest.WindSpeed AS CellNorthwestWindSpeed,gpNorthwest.WindDirection AS CellNorthwestWidDir,"
            "gpNorthwest.DewPointTemperature AS CellNorthwestDewPoint,gpNorthwest.AirPressure AS CellNorthwestAirPressure,gpNorthwest.RelativeHumidity AS CellNorthwestRelativeHumidity,"
            "gpNortheast.Temperature AS CellNortheastTemp,gpNortheast.PrecipitationRate AS CellNortheastPrecipRate,gpNortheast.Visibility AS CellNortheastVis,"
            "gpNortheast.WindSpeed AS CellNortheastWindSpeed,gpNortheast.WindDirection AS CellNortheastWidDir,"
            "gpNortheast.DewPointTemperature AS CellNortheastDewPoint,gpNortheast.AirPressure AS CellNortheastAirPressure,gpNortheast.RelativeHumidity AS CellNortheastRelativeHumidity,"
            "gpSoutheast.Temperature AS CellSoutheastTemp,gpSoutheast.PrecipitationRate AS CellSoutheastPrecipRate,gpSoutheast.Visibility AS CellSoutheastVis,"
            "gpSoutheast.WindSpeed AS CellSoutheastWindSpeed,gpSoutheast.WindDirection AS CellSoutheastWidDir,"
            "gpSoutheast.DewPointTemperature AS CellSoutheastDewPoint,gpSoutheast.AirPressure AS CellSoutheastAirPressure,gpSoutheast.RelativeHumidity AS CellSoutheastRelativeHumidity,"
            "gpSouthwest.Temperature AS CellSouthwestTemp,gpSouthwest.PrecipitationRate AS CellSouthwestPrecipRate,gpSouthwest.Visibility AS CellSouthwestVis,"
            "gpSouthwest.WindSpeed AS CellSouthwestWindSpeed,gpSouthwest.WindDirection AS CellSouthwestWidDir,"
            "gpSouthwest.DewPointTemperature AS CellSouthwestDewPoint,gpSouthwest.AirPressure AS CellSouthwestAirPressure,gpSouthwest.RelativeHumidity AS CellSouthwestRelativeHumidity ")

    # add target hour
    query += f', sr{h}.SR as SR{h} '

    # add FROM and JOINs
    query += " from solarradiation sr "
    query += f' INNER JOIN solarradiation sr{h} ON sr{h}.id=sr.id+{h*4} and sr.SiteID=sr{h}.SiteID '
    query += f' INNER JOIN gribprediction gp ON gp.SolarRadiationID=sr{h}.id AND (gp.Datasource="rap" OR gp.Datasource="rapinterpolation") ' \
             f' AND gp.HoursAhead=1 AND gp.cell="" and gp.SiteID=sr{h}.siteID '

    if window:
        query += f' INNER JOIN solarradiation psr1 ON psr1.id=sr.id-4' \
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

    if nam_grid:
        query += " INNER JOIN gribprediction gpWest ON gpWest.SolarRadiationID=sr.id AND " \
                 " (gpWest.Datasource='rap' OR gpWest.Datasource='rapinterpolation') AND gpWest.HoursAhead=1 " \
                 " AND gpWest.cell='West' AND gp.SiteID=gpWest.SiteID" \
                 " INNER JOIN gribprediction gpEast ON gpEast.SolarRadiationID=sr.id AND " \
                 " (gpEast.Datasource='rap' OR gpEast.Datasource='rapinterpolation') AND gpEast.HoursAhead=1 " \
                 " AND gpEast.cell='East' AND gp.SiteID=gpEast.SiteID" \
                 " INNER JOIN gribprediction gpNorth ON gpNorth.SolarRadiationID=sr.id AND " \
                 " (gpNorth.Datasource='rap' OR gpNorth.Datasource='rapinterpolation') AND gpNorth.HoursAhead=1 " \
                 " AND gpNorth.cell='North' AND gp.SiteID=gpNorth.SiteID" \
                 " INNER JOIN gribprediction gpSouth ON gpSouth.SolarRadiationID=sr.id AND " \
                 " (gpSouth.Datasource='rap' OR gpSouth.Datasource='rapinterpolation') AND gpSouth.HoursAhead=1 " \
                 " AND gpSouth.cell='South' AND gp.SiteID=gpSouth.SiteID" \
                 " INNER JOIN gribprediction gpNorthwest ON gpNorthwest.SolarRadiationID=sr.id AND " \
                 " (gpNorthwest.Datasource='rap' OR gpNorthwest.Datasource='rapinterpolation') AND gpNorthwest.HoursAhead=1 " \
                 " AND gpNorthwest.cell='Northwest' AND gp.SiteID=gpNorthwest.SiteID" \
                 " INNER JOIN gribprediction gpNortheast ON gpNortheast.SolarRadiationID=sr.id AND " \
                 " (gpNortheast.Datasource='rap' OR gpNortheast.Datasource='rapinterpolation') AND gpNortheast.HoursAhead=1 " \
                 " AND gpNortheast.cell='Northeast' AND gp.SiteID=gpNortheast.SiteID" \
                 " INNER JOIN gribprediction gpSouthwest ON gpSouthwest.SolarRadiationID=sr.id AND " \
                 " (gpSouthwest.Datasource='rap' OR gpSouthwest.Datasource='rapinterpolation') AND gpSouthwest.HoursAhead=1 " \
                 " AND gpSouthwest.cell='Southwest' AND gp.SiteID=gpSouthwest.SiteID" \
                 " INNER JOIN gribprediction gpSoutheast ON gpSoutheast.SolarRadiationID=sr.id AND " \
                 " (gpSoutheast.Datasource='rap' OR gpSoutheast.Datasource='rapinterpolation') AND gpSoutheast.HoursAhead=1 " \
                 " AND gpSoutheast.cell='Southeast' AND gp.SiteID=gpSoutheast.SiteID "

    # add date and size constraints
    query += f' WHERE sr.dateandtime BETWEEN "{start_date}" AND "{end_date}" AND sr.SiteID={site_id} ' \
             f' ORDER BY sr.dateandtime LIMIT 100000;'

    return query