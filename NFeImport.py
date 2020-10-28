#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
NFeImport.py

MM-DD-YYYY
08-06-2018 : Ajuste no layout para o NFe 4.0
08-10-2018 : Correcao para NF com apenas 01 item
09-05-2018 : Ajuste para importar NFe
09-14-2018 : Ajuste para importar NFe antes da v4.0
28-10-2020 : 
  infAdProd para quando nao tem valor informar 0.00
  adicionado 05 novos campos:
    modBCST
    pMVAST
    vBCST
    pICMSST
    vICMSST
  NFeXML.py
    Campos passaram a ser opcionais:
      marca
      nVol
'''

import os
from os import urandom
import shutil
import sys

import logging
import logging.config

from NFeSQL import selectNFe, insertNFe
from NFeXML import extractNFeData, extractNFeDetail

def main():
  
  logging.config.fileConfig('logconf/logging.conf', defaults={'logfilename': 'log/nfeimport.log'})
  logger = logging.getLogger('NFeImport')
  
  if len(sys.argv) - 1 == 0:
    print("Path com os XMLs nao informado.")
    logger.error('Path com os XMLs nao informado.')
    
    '''
    # log something
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
    '''

    sys.exit(0)

  path = sys.argv[1]

  xml_files = [x for x in os.listdir(path) if (x.startswith("SY3_X")) and (x.endswith(".xml"))]

  for xml in xml_files:

    documentXML = path+xml

    logger.info("Processando: %s " , documentXML)

    extractNFeDataResult = extractNFeData(documentXML)
    extractNFeDetailResult = extractNFeDetail(documentXML)

    selectNFe(extractNFeDataResult)
    insertNFe(extractNFeDataResult, extractNFeDetailResult)

    src = documentXML
    dest = path+'done/'+xml

    # move file after processed
    shutil.move(src, dest)  

#
# Main module
#
if __name__ == "__main__":
  main()

