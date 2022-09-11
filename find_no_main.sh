#!/bin/bash

pss --py -L "def main\(\):" --exclude-pattern "(__init__|logs|Files|filters|forms|Debug|Notificador|test_.+|urls|Utils|Html|Form|Database|Mensajeria|Controles|Validar|Menu|View|Cache|Notas)\.py"
