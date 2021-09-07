#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 21:13:25 (CST) daisuke>
#

# importing csv module
import csv

# importing sqlite3 module
import sqlite3

# CSV file
file_csv = 'elements.csv'

# database file
file_db = 'elements.db'

# SQL command to make a table
sql_maketable  = 'create table elements'
sql_maketable += ' (AtomicNumber integer primary key, Element text,'
sql_maketable += ' Symbol text, AtomicWeight real, ElementPeriod integer,'
sql_maketable += ' ElementGroup integer, Phase text, MostStableCrystal text,'
sql_maketable += ' Type text, IonicRadius real, AtomicRadius real,'
sql_maketable += ' ElectronNegativity real, FirstIonizationPotential real,'
sql_maketable += ' Density real, MeltingPoint real, BoilingPoint real,'
sql_maketable += ' Isotopes integer, Discoverer text, DiscoveryYear integer,'
sql_maketable += ' SpecificHeatCapacity real, ElectronConfiguration text);'

# connection to database
conn = sqlite3.connect (file_db)
c = conn.cursor ()

# making a table
c.execute (sql_maketable)

# opening file
with open (file_csv, 'r', encoding='latin_1') as fh:
    # reading CSV file
    reader = csv.reader (fh)
    # processing each row
    for row in reader:
        # if the line does not start with number, then we skip it.
        if not (row[0].isdecimal ()):
            continue

        # splitting data
        (AtomicNumber, Element, Symbol, AtomicWeight, ElementPeriod, \
         ElementGroup, Phase, MostStableCrystal, Type, IonicRadius, \
         AtomicRadius, ElectronNegativity, FirstIonizationPotential, Density, \
         MeltingPoint, BoilingPoint, Isotopes, Discoverer, DiscoveryYear, \
         SpecificHeatCapacity, ElectronConfiguration, Row, Column) \
         = row

        # replacing some data
        if (MostStableCrystal == ''):
            MostStableCrystal = '__NONE__'
        if (IonicRadius == ''):
            IonicRadius = -99.99
        if (ElectronNegativity == ''):
            ElectronNegativity = -99.99
        if (MeltingPoint == ''):
            MeltingPoint = -99.99
        if (BoilingPoint == ''):
            BoilingPoint = -99.99
        if ( (DiscoveryYear == 'Prehistoric') or (DiscoveryYear == '') ):
            DiscoveryYear = '-9999'
        if (SpecificHeatCapacity == ''):
            SpecificHeatCapacity = -99.99
        if (AtomicRadius == ''):
            AtomicRadius = -99.99
        if (Density == ''):
            Density = -99.99
        if (FirstIonizationPotential == ''):
            FirstIonizationPotential = -99.99
        if (Isotopes == ''):
            Isotopes = -9999

        # conversion from string into int or float
        AtomicNumber             = int (AtomicNumber)
        AtomicWeight             = float (AtomicWeight)
        ElementPeriod            = int (ElementPeriod)
        ElementGroup             = int (ElementGroup)
        IonicRadius              = float (IonicRadius)
        AtomicRadius             = float (AtomicRadius)
        ElectronNegativity       = float (ElectronNegativity)
        FirstIonizationPotential = float (FirstIonizationPotential)
        Density                  = float (Density)
        MeltingPoint             = float (MeltingPoint)
        BoilingPoint             = float (BoilingPoint)
        Isotopes                 = int (Isotopes)
        DiscoveryYear            = int (DiscoveryYear)
        SpecificHeatCapacity     = float (SpecificHeatCapacity)

        # SQL command to add data to table
        sql_adddata  = "insert into elements values (%d, \"%s\", \"%s\"," \
            % (AtomicNumber, Element, Symbol)
        sql_adddata += " %f, %d, %d, \"%s\", \"%s\", \"%s\"," \
            % (AtomicWeight, ElementPeriod, ElementGroup, Phase, \
               MostStableCrystal, Type)
        sql_adddata += " %f, %f, %f, %f, %f, %f, %f, %d," \
            % (IonicRadius, AtomicRadius, ElectronNegativity, \
               FirstIonizationPotential, Density, MeltingPoint, BoilingPoint, \
               Isotopes)
        sql_adddata += " \"%s\", %d, %f, \"%s\");" \
            % (Discoverer, DiscoveryYear, SpecificHeatCapacity, \
               ElectronConfiguration)

        # executing a SQL command to add data into table
        c.execute (sql_adddata)

# commit
conn.commit ()

# closing the connection to database
conn.close()
