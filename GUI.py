# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 14:02:48 2020

@author: paul-
"""

import wx
import os
import osmnx as ox
from shapely.geometry import Point
import mplleaflet 

class Utform(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, wx.ID_ANY, title='Tool')

        
        self.panel = wx.Panel(self, wx.ID_ANY)

        title = wx.StaticText(self.panel, wx.ID_ANY, 'Find POI')

        labelone = wx.StaticText(self.panel, wx.ID_ANY, 'location', size=(100, 20))
        self.inputtxtone = wx.TextCtrl(self.panel, wx.ID_ANY, '', size=(200, 20))

        labeltwo = wx.StaticText(self.panel, wx.ID_ANY, 'radius', size=(100, 20))
        self.inputtxttwo = wx.TextCtrl(self.panel, wx.ID_ANY, '', size=(200, 20))

        labelthree = wx.StaticText(self.panel, wx.ID_ANY, 'keywords', size=(100, 20))
        self.inputtxtthree = wx.TextCtrl(self.panel, wx.ID_ANY, '', size=(200, 20))
            
        okbtn = wx.Button(self.panel, wx.ID_ANY, 'OK')
        cancelbtn = wx.Button(self.panel, wx.ID_ANY, 'Cancel')

        self.inputtxtone.Bind(wx.EVT_KILL_FOCUS, self.input1)
        self.inputtxttwo.Bind(wx.EVT_KILL_FOCUS, self.input2)
        self.inputtxtthree.Bind(wx.EVT_KILL_FOCUS, self.input3)

        self.Bind(wx.EVT_BUTTON, self.get_geom_from_osm, okbtn)
        self.Bind(wx.EVT_BUTTON, self.oncancel, cancelbtn)
        
        topsizer = wx.BoxSizer(wx.VERTICAL)
        titlesizer = wx.BoxSizer(wx.VERTICAL)
        inputonesizer = wx.BoxSizer(wx.HORIZONTAL)
        inputtwosizer = wx.BoxSizer(wx.HORIZONTAL)
        inputthreesizer = wx.BoxSizer(wx.HORIZONTAL)

        btnsizer = wx.BoxSizer(wx.HORIZONTAL)

        titlesizer.Add(title, 0, wx.ALL, 5)

        inputonesizer.Add(labelone, 0, wx.ALL, 5)
        inputonesizer.Add(self.inputtxtone, 0, wx.ALL | wx.EXPAND, 5)

        inputtwosizer.Add(labeltwo, 0, wx.ALL, 5)
        inputtwosizer.Add(self.inputtxttwo, 0, wx.ALL | wx.EXPAND, 5)

        inputthreesizer.Add(labelthree, 0, wx.ALL, 5)
        inputthreesizer.Add(self.inputtxtthree, 0, wx.ALL | wx.EXPAND, 5)
        
        btnsizer.Add(okbtn, 1, wx.ALL, 5)
        btnsizer.Add(cancelbtn, 1, wx.ALL, 5)

        topsizer.Add(titlesizer, 0, wx.CENTER)
        topsizer.Add(wx.StaticLine(self.panel, ), 0, wx.ALL | wx.EXPAND, 5)

        topsizer.Add(inputonesizer, 0, wx.ALL | wx.EXPAND, 5)
        topsizer.Add(inputtwosizer, 0, wx.ALL | wx.EXPAND, 5)
        topsizer.Add(inputthreesizer, 0, wx.ALL | wx.EXPAND, 5)
        topsizer.Add(btnsizer, 0, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(topsizer)

        customerpath = os.path.abspath(".")
        self.CreateStatusBar()
        self.SetStatusText(customerpath)

    def input1(self, event):
        location = self.inputtxtone.GetValue()
        print(location)
    
    def input2(self, event):
        radius = self.inputtxttwo.GetValue()
        print(radius)
        
    def input3(self, event):
        keywords = self.inputtxtthree.GetValue()
        print(keywords)
        
    def oncancel(self, event):
        print("cancelled")
        
        
    def get_geom_from_osm(self, event):
        
        location = self.inputtxtone.GetValue()
        radius = int(self.inputtxttwo.GetValue())
        keyword = self.inputtxtthree.GetValue()
        
        # check type of first parameter 'location'
        assert isinstance(location, str), "Input location needs to be a string!"
    
        #check type and value of second parameter 'radius'
        assert isinstance(radius, (int, float)), "Input radius needs to be integer or floating number!"  
        assert radius > 0, "Radius needs to be higher than 0"
    
        # check type of third parameter 'tags'
        assert isinstance(keyword, (str, list)), "Input tags needs to be a string or list!"
    
        # check if keyword is a list and convert a single keyword in a list 
        if isinstance(keyword, list):
        
            assert len(keyword) <= 5, "Input list itmes needs to be less than 5"
       
        else:
            keyword = [keyword]
        
        print("Input types are correct")
    
    
        # get all geometries from osm inside the radius 
        geom = ox.geometries.geometries_from_address(
            address = location, 
            tags = {'buildings':True,'amenity':True}, 
            dist = radius
            )

        # List for selected buildings
        target_list = []
    
        # loop over geom-table rows
        for idx, row in geom.iterrows():
        
            # loop over columns for each row
            for column in geom.columns:
            
                # if the keywords are in the column, append the osmid into an target list
                if geom.at[idx, column] in keyword:
                
                    target_list.append(geom.at[idx, 'osmid'])
                    print("Found:" +  geom.at[idx, column] + " at ", geom.at[idx, 'addr:street'])
        
                else:
                    continue 
    
        # select geom from target_list
        geom = geom.loc[geom['osmid'].isin(target_list)]
    
        # drop every non-value column and the column 'nodes'
        geom = geom.dropna(axis=1, how='all')
        
        try:
            geom = geom.drop(['nodes'], axis=1)        
        
        except:
           print('Column nodes not in dataframe')
           
        # transfer polygon in point geometry
        for idx, rows in geom.iterrows():
        
            if not isinstance(geom.at[idx, 'geometry'], Point):
            
                geom.at[idx, 'geometry'] = geom.at[idx, 'geometry'].centroid
        
            else:
                continue
            
        # Set correct CRS
        geom = geom.to_crs(epsg=25832)
        
        # Show results
        print("Found " + str(len(geom)) + " geometries")
        
        outfn = "geom_" + str(keyword[0]) + ".shp"
        folder = r"C:\Users\paul-\Desktop\AutoGIS\Final_plugin"
        
        outfp = os.path.join(folder, outfn)
        
        geom.to_file(outfp)
    
        print("Saved SHP in: ", outfp)
        
        
        
        
if __name__ == '__main__':
    app = wx.App()
    frame = Utform().Show()
    app.MainLoop()
    
