# Chatbot Resiliente Multi-Proveedor

Este proyecto es un chatbot en Python basado en consola que integra OpenAI, Anthropic Claude y Google Gemini. Presenta una arquitectura tolerante a fallos, lo que le permite realizar "fallback" si la API de un proveedor cae o agota sus cuotas.

## Cómo ejecutar

1. Instala las dependencias: `pip install -r requirements.txt`
2. Configura las claves de los proveedores en un archivo `.env`
3. Ejecuta el chatbot interactivo: `python main.py`
4. Teclea `/salir` cuando termines.


get_accounts_csv_all <- function(con = NULL, partition_key, model_name, account_table, agg_var_names, acc_var_names, group) {
  
  print(paste0(Sys.time(), " - Loading Accounts from CSV (Group ", group, ")"))
  
  # 1. Cargar el CSV
  file_path <- paste0("/data/x617119/notebook/Leire/", account_table, ".csv")
  ACCOUNTS <- fread(file_path, nThread = 2)
  
  # 2. FILTRO BASE (partition_key para todos los grupos)
  if ("partition_key" %in% names(ACCOUNTS)) {
    ACCOUNTS <- ACCOUNTS[partition_key == ..partition_key] 
  }
  
  # 3. FILTRO DE MODELO (Solo para grupos 0 al 7)
  # Replicamos el SUBSTR e INSTR de SQL limpiando todo desde el caracter '|'
  if (group != 8) {
    ACCOUNTS <- ACCOUNTS[sub("\\|.*", "", PORT_ID) == model_name]
  }
  
  # 4. LÓGICA DE SELECCIÓN Y AGRUPACIÓN POR GRUPO
  if (group == 0) {
    target_cols <- c("ACC_ID", "PORT_ID", "END_DATE", "STATE", agg_var_names, acc_var_names)
    cols_to_select <- intersect(target_cols, names(ACCOUNTS))
    ACCOUNTS <- ACCOUNTS[, ..cols_to_select]
    
  } else if (group == 1) {
    # El grupo 1 es especial: requiere agrupar (GROUP BY) y sumar (SUM)
    grp_cols <- c("PORT_ID", "END_DATE", "STATE", acc_var_names)
    cols_to_group <- intersect(grp_cols, names(ACCOUNTS))
    cols_to_sum <- intersect(agg_var_names, names(ACCOUNTS))
    
    ACCOUNTS <- ACCOUNTS[, lapply(.SD, sum, na.rm = TRUE), by = cols_to_group, .SDcols = cols_to_sum]
    
    # Creamos un ACC_ID sintético (replicando el row_number() de SQL)
    setorderv(ACCOUNTS, cols_to_group)
    ACCOUNTS[, ACC_ID := .I]
    
  } else if (group == 2) {
    target_cols <- c("ACC_ID", "PORT_ID", "END_DATE", agg_var_names, acc_var_names)
    cols_to_select <- intersect(target_cols, names(ACCOUNTS))
    ACCOUNTS <- ACCOUNTS[, ..cols_to_select]
    
  } else if (group == 3) {
    target_cols <- c("ACC_ID", "PORT_ID", "END_DATE", "COUNT_ACC", agg_var_names, acc_var_names)
    cols_to_select <- intersect(target_cols, names(ACCOUNTS))
    ACCOUNTS <- ACCOUNTS[, ..cols_to_select]
    
  } else if (group == 4) {
    target_cols <- c("ACC_ID", "PORT_ID", "END_DATE", "FECHAPER", "FECHAEXP", agg_var_names, acc_var_names)
    cols_to_select <- intersect(target_cols, names(ACCOUNTS))
    ACCOUNTS <- ACCOUNTS[, ..cols_to_select]
    
  } else if (group == 5) {
    target_cols <- c("ACC_ID", "PORT_ID", "END_DATE", "STATE", "COUNT_ACC", agg_var_names, acc_var_names)
    cols_to_select <- intersect(target_cols, names(ACCOUNTS))
    ACCOUNTS <- ACCOUNTS[, ..cols_to_select]
    
  } else if (group == 6) {
    target_cols <- c("ACC_ID", "PORT_ID", "END_DATE", "STATE", "COUNT_ACC", "Q_DEF", agg_var_names, acc_var_names)
    cols_to_select <- intersect(target_cols, names(ACCOUNTS))
    ACCOUNTS <- ACCOUNTS[, ..cols_to_select]
    
  } else if (group == 7) {
    target_cols <- c("ACC_ID", "PORT_ID", "END_DATE", "STATE", "B_MORA", "Q_DEF", agg_var_names, acc_var_names)
    cols_to_select <- intersect(target_cols, names(ACCOUNTS))
    ACCOUNTS <- ACCOUNTS[, ..cols_to_select]
    
  } else if (group == 8) {
    target_cols <- c("ACC_ID", "PORT_ID", "END_DATE", "STATE", "B_MORA", "Q_DEF", "PRODUCTO", agg_var_names, acc_var_names)
    cols_to_select <- intersect(target_cols, names(ACCOUNTS))
    ACCOUNTS <- ACCOUNTS[, ..cols_to_select]
  }
  
  # 5. FORMATEAR LA FECHA 
  if ("END_DATE" %in% names(ACCOUNTS)) {
    ACCOUNTS[, END_DATE := as.Date(format(as.Date(END_DATE), tz = "CET"), usetz = FALSE)]
  }
  
  # 6. ORDENAR Y SETEAR KEYS (Optimizamos la memoria para R)
  setkeyv(ACCOUNTS, intersect(c("END_DATE", "ACC_ID"), names(ACCOUNTS)))
  
  return(ACCOUNTS)
}
