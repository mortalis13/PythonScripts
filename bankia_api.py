import os, re, codecs, subprocess, json
import shutil, stat, errno, sys, http, time
import requests

from datetime import datetime, timedelta
from getpass import getpass
from pprint import pprint
from base64 import b64decode, b64encode

# pip install pycryptodome
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


# Show the account balance and last operations


def run():
  headers_common = {
    'x-j_gid_cod_app': 'o3',
    'j_gid_cod_app': 'o3',
    'j_gid_cod_ds': 'oip',
    'j_gid_indice': 'null',
  }
  
  # ---------------
  usr = getpass('')
  psw = getpass('')
  # ------
  # with open('_files/ubp.txt') as f: usr = f.read()
  # with open('_files/pbu.txt') as f: psw = f.read()
  # ------
  # usr = '123'
  # psw = '1234'
  # ---------------
  
  
  # === [KEY] ===
  print('\n>> Calling /key')
  response = requests.get('https://www.bankia.es/api/1.0/login/key', headers=headers_common)
  res = response.json()
  
  if not res or not 'j_gid_response_lt' in res:
    print('\n..ERROR /key')
    print(res)
    return
  
  j_gid_response_lt = res['j_gid_response_lt']
  j_gid_response_rsa = res['j_gid_response_rsa']
  
  # --- Encrypt pass with RSA key
  key = j_gid_response_rsa
  
  key = b64decode(key)
  key = RSA.importKey(key, passphrase=None)
  
  cipher = PKCS1_v1_5.new(key)
  res = cipher.encrypt(psw.encode())
  
  j_gid_password = b64encode(res).decode()
  # ---
  
  
  # === [LOGIN] ===
  headers = headers_common.copy()
  headers['Cookie'] = 'SSO_TL_OIP=' + j_gid_response_lt
  headers['Content-Type'] = 'application/x-www-form-urlencoded'
  
  data = {
    'j_gid_action': 'login',
    'j_gid_cod_app': 'o3',
    'j_gid_cod_ds': 'oip',
    'j_gid_num_documento': usr,
    'j_gid_password': j_gid_password,
  }
  
  print('\n>> Calling /login')
  print('  headers:')
  print(headers)
  print('  data:')
  print(data)
  
  response = requests.post('https://www.bankia.es/api/1.0/escenario/escenarioaplicacion/login', headers=headers, data=data)
  res = response.json()
  
  if not res or not 'j_gid_response_tgt' in res:
    print('\n..ERROR /login')
    print(res)
    return
  
  j_gid_response_tgt = res['j_gid_response_tgt']
  
  
  # === [INFO] ===
  headers = headers_common.copy()
  headers['Cookie'] = 'SSO_TGT_OIP=' + j_gid_response_tgt
  
  # -- Needed to call '/contratos' and '/movimiento-grid'
  print('\n>> Calling /escenarioaplicacion')
  response = requests.get('https://www.bankia.es/api/1.0/servicios/escenario.escenarioaplicacion/5.0/escenario/escenarioaplicacion', headers=headers)
  
  print('\n>> Calling /escenariocliente')
  response = requests.get('https://www.bankia.es/api/1.0/servicios/contexto.escenariocliente/13.0/contexto/escenariocliente?_ts1590913923649', headers=headers)
  
  
  # ====== Contracts
  print('\n>> Calling /contratos')
  print('  headers:')
  print(headers)
  response = requests.get('https://www.bankia.es/api/1.0/servicios/contratos/9.0/contratos?groupByFamilia=true&idVista=1', headers=headers)
  res = response.json()
  
  if not res or not 'listaCuentas' in res:
    print('\n..ERROR /contratos')
    print(res)
    return
  
  cuenta = res['listaCuentas'][0]
  identificadorContratoProducto = res['listaCuentas'][0]['contrato']['identificadorContratoProducto']
  
  saldoDisponible_importeConSigno        = cuenta['saldoDisponible']['importeConSigno']
  saldoDisponible_numeroDecimalesImporte = cuenta['saldoDisponible']['numeroDecimalesImporte']
  saldoReal_importeConSigno              = cuenta['saldoReal']['importeConSigno']
  saldoReal_numeroDecimalesImporte       = cuenta['saldoReal']['numeroDecimalesImporte']
  
  try:
    saldoDisponible_numeroDecimalesImporte = int(saldoDisponible_numeroDecimalesImporte)
    if saldoDisponible_numeroDecimalesImporte > 0:
      saldoDisponible_importeConSigno /= (10**saldoDisponible_numeroDecimalesImporte)
    
    saldoReal_numeroDecimalesImporte = int(saldoReal_numeroDecimalesImporte)
    if saldoReal_numeroDecimalesImporte > 0:
      saldoReal_importeConSigno /= (10**saldoReal_numeroDecimalesImporte)
  except:
    print('\n..ERROR during conversion')
    print('saldoDisponible_importeConSigno:', saldoDisponible_importeConSigno)
    print('saldoDisponible_numeroDecimalesImporte:', saldoDisponible_numeroDecimalesImporte)
    print('saldoReal_importeConSigno:', saldoReal_importeConSigno)
    print('saldoReal_numeroDecimalesImporte:', saldoReal_numeroDecimalesImporte)
  
  
  # ====== Operations
  print('\n>> Calling /movimiento-grid')
  fechaOperacionDesde = (datetime.now() + timedelta(days=-60)).strftime('%Y-%m-%d')
  fechaOperacionHasta = datetime.now().strftime('%Y-%m-%d')
  LIM_OPERATIONS = 10
  
  data = {
    "identificadorCuenta": {
      "identificador": identificadorContratoProducto[4:]
    },
    "criteriosBusquedaCuenta": {
      "cantidadUltimosMovimientos": LIM_OPERATIONS
    }
  }
  data = json.dumps(data)
  print('  data:')
  print(data)
  
  headers['Content-Type'] = 'application/json'
  
  response = requests.post('https://www.bankia.es/api/1.0/servicios/cuenta.movimiento-grid/2.0/cuenta/movimiento-grid', headers=headers, data=data)
  res = response.json()
  
  if not res or not 'movimientos' in res:
    print('\n..ERROR /movimiento-grid')
    print(res)
    return
  
  ops = []
  movimientos = res['movimientos']
  for mov in movimientos:
    concepto        = mov['conceptoMovimiento']['descripcionConcepto']
    fecha           = mov['fechaMovimiento']['valor']
    importe         = mov['importe']['importeConSigno']
    numeroDecimales = mov['importe']['numeroDecimales']
    
    try:
      importe = importe/(10**numeroDecimales) if numeroDecimales > 0 else importe
    except:
      print('..ERROR during conversion')
      print('importe:', importe)
    
    ops.append('{:<+6.2f} :: {} :: "{}"'.format(importe, fecha, concepto))
    # ops.append('{} :: {} :: "{}"'.format('{:+06.2f}'.format(importe), fecha, concepto))
    
  
  # ====== OUTPUT
  print('\n\n------------------------------\n[RESULT]')
  print('saldoReal      :', saldoReal_importeConSigno)
  print('saldoDisponible:', saldoDisponible_importeConSigno)
  
  print('\n== OPERATIONS')
  [print(op) for op in ops]


# ------
run()
