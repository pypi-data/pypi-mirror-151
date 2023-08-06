# -*- coding: utf-8 -*-

import med_data_science_helper.helper_terceros_kpi as htk
import med_data_science_helper.helper_acces_db as hadb


df_siagie = hadb.get_siagie_por_anio(2021,id_nivel="F0",columns_n= ['ID_PERSONA',"COD_MOD"])
df_siagie2 = htk.agregar_nexus(df_siagie,anio_df=2021,anio_h=2021, cache=False )
