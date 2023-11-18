import arcpy

# To allow overwriting outputs change overwriteOutput option to True.
arcpy.env.overwriteOutput = True

# Check out any necessary licenses.
arcpy.CheckOutExtension("Spatial")

# The input parameters for the tool
LandUse = arcpy.GetParameterAsText(0)
Streams = arcpy.GetParameterAsText(1)
Elevation = arcpy.GetParameterAsText(2)

# The output parameter for the tool
Output = arcpy.GetParameterAsText(3)

####################
#Habitat Sub-Model:

# Process: Euclidean Distance (Euclidean Distance) (sa)
# Calculates the distance for the cells to the streams
Streamdistance = arcpy.sa.EucDistance(in_source_data=Streams, maximum_distance=None, cell_size="30", distance_method="PLANAR", in_barrier_data="")


# Process: Rescale by Function (2) (Rescale by Function) (sa)
# Re-Scales the streams raster from 1-10 with farther values from the stream being lower numbers (1, 2, 3 etc) and closer values to the stream being higher numbers (10, 9, 8, etc) 
Rescaled_Streams_Raster = arcpy.sa.RescaleByFunction(in_raster=Streamdistance, transformation_function=[["MSSMALL", "", "", "", "", "", "", ""]], from_scale=1, to_scale=10)



# Process: Slope (Slope) (sa)
# Calculates the slopes of the elevation raster
Slope_Raster = arcpy.sa.Slope(in_raster=Elevation, output_measurement="DEGREE", method="PLANAR")



# Process: Rescale by Function (Rescale by Function) (sa)
# Re-Scales the slope raster from 1-10 with smaller slope values being lower numbers (1, 2, 3, etc) and steeper slopes values being higher values (10, 9, 8, etc)
Rescaled_Slope_Raster = arcpy.sa.RescaleByFunction(in_raster=Slope_Raster, transformation_function=[["LogisticGrowth", "", "", "", "", "", "", ""]], from_scale=1, to_scale=10)



# Process: Reclassify (Reclassify) (sa)
# Re-Classifies the land use raster based on ideal habitats for the Bobcat (Forest land being preffered so it is given higher values (10,9))
Reclassified_LandUse_Raster = arcpy.sa.Reclassify(in_raster=LandUse, reclass_field="VALUE", remap="1 1;2 1;3 1;4 4;5 5;6 9;7 9;8 10;9 6;10 5;11 3;12 2", missing_values="DATA")



# Process: Weighted Sum (Weighted Sum) (sa)
# Weighs the Streams, Slopes, and LandUse to make Habitat Submodel. LandUse is given a bit more weight since it is most important factor to consider compared to others
Habitat_WeightedSum = arcpy.sa.WeightedSum(arcpy.sa.WSTable([[Rescaled_Streams_Raster, "VALUE", 1], [Rescaled_Slope_Raster, "VALUE", 1], [Reclassified_LandUse_Raster, "Value", 2]]))



####################
#Food Sub-Model:

# Process: Reclassify (2) (Reclassify) (sa)
# Re-classifies the LandUse based on most suitable areas for Bobcat to find food (Forestland and Grassland being higher values with 10, 9)
Food_Reclassify = arcpy.sa.Reclassify(in_raster=LandUse, reclass_field="VALUE", remap="1 1;2 1;3 1;4 5;5 9;6 9;7 9;8 10;9 4;10 4;11 2;12 2", missing_values="DATA")



####################
#Security Sub-Model:

# Process: Extract by Attributes (Extract by Attributes) (sa)
# Extracts the urban areas from the data since it contains houses, roads, human development, etc which will be used for security sub-model
UrbanAreas = arcpy.sa.ExtractByAttributes(in_raster=LandUse, where_clause="VALUE = 1 OR VALUE = 2 OR VALUE = 3")


# Process: Euclidean Distance (2) (Euclidean Distance) (sa)
# Calculates the distance for the cells to the urban areas
Urban_Distance = arcpy.sa.EucDistance(in_source_data=UrbanAreas, maximum_distance=None, cell_size="30", distance_method="PLANAR", in_barrier_data="")


# Process: Rescale by Function (3) (Rescale by Function) (sa)
# Re-Scales the raster from 1-10 with cells farther away from urban areas being more preffered. Farther cells have higher values (8, 9, 10, etc)
Urban_Rescaled = arcpy.sa.RescaleByFunction(in_raster=Urban_Distance, transformation_function=[["LogisticGrowth", "", "", "", "", "", "", ""]], from_scale=1, to_scale=10)


####################
#Final Suitability Model:


# Process: Weighted Sum (2) (Weighted Sum) (sa)
# Weighs each of the sub-models equally as they are all of importance and gives a final suitability raster
FinalSuitability = arcpy.sa.WeightedSum(arcpy.sa.WSTable([[Habitat_WeightedSum, "VALUE", 1], [Food_Reclassify, "Value", 1], [Urban_Rescaled, "VALUE", 1]]))


# Process: Locate Regions (Locate Regions) (sa)
# Locates 5 suitable regions (can set more or less based on needs) that are at least 10 contiguous square kilometers
Suitable_Regions = arcpy.sa.LocateRegions(in_raster=FinalSuitability, total_area=50, area_units="SQUARE_KILOMETERS", number_of_regions=5, region_shape="CIRCLE", region_orientation=0, shape_tradeoff=50, evaluation_method="HIGHEST_AVERAGE_VALUE", minimum_area=10, maximum_area=None, minimum_distance=None, maximum_distance=None, distance_units="KILOMETERS", in_existing_regions="", number_of_neighbors="EIGHT", no_islands="NO_ISLANDS", region_seeds="AUTO", region_resolution="AUTO", selection_method="AUTO")
Suitable_Regions.save(Output)


