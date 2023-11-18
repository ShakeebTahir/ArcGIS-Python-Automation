<h1>Vermont Bobcat Suitability Analysis</h1>

<h2>Description</h2>
Automated the process of finding the most suitable areas to re-locate Bobcats by creating a custom ArcGIS tool using Python. This project uses an area of Vermont as the use case but the tool could be applied to any other area such as within other states like Minnesota, Colorado, etc., as long as you have the relevant datasets for that area.
<br />


<h2>Tools used to complete project</h2>

- <b>Python</b>
- <b>ArcPy</b> 
- <b>ArcGIS Pro</b>

<h2>Required Data Sets</h2>

- <b>Elevation</b>
- <b>Streams</b> 
- <b>Land Use</b>
<p>Data Source: Vermont Open Geodata Portal</p>

<h2>Methodology</h2>
<p>3 Submodels were created based on the datasets:

Habitat - Areas where Bobcats prefer to live

Food - Areas where Bobcat is most likely to find food

Security - Areas where the Bobcat is away from human development and disruption

------------------------------------------------------------------------------------

1\. Found the habitat of bobcats by finding the nearest streams and steepest areas.

- Found closest streams by using the Euclidean Distance tool.
- Found the steepest areas by using the slope tool and statistically rescaled the steep areas.

2\. Separated the food areas and urban areas.
- Found the areas where the bobcats can easily find food by ordering the land type using the Reclassify tool.
- Found the urban/developed areas using the Extract by Attributes tool and used Euclidean Distance tool to find the farthest safe/food places.

3\. Combined all these conditions by using the Weighted Sum tool. The final map or result will show the most safe places with food and water for bobcats

<br/>
<p align="center">
Flowchart:
<br/>
<img src="https://github.com/ShakeebTahir/ArcGIS-Python-Automation/assets/32227140/fd2e1d1c-755a-4ec4-a1b0-e366c5a1b699" height="80%" width="80%"/>

<h2>Walk-Through:</h2>

<p align="center">
Elevation Data Set: 
<br/>
<img src="https://github.com/ShakeebTahir/ArcGIS-Python-Automation/assets/32227140/80263118-e910-4efd-85f5-9d4dad0ff377" height="80%" width="80%"/>
<br />
<br />
Streams Data Set:  <br/>
<img src="https://github.com/ShakeebTahir/ArcGIS-Python-Automation/assets/32227140/3e16a6bb-7d8f-434c-aab1-037c72e19259" height="80%" width="80%"/>
<br />
<br />
Land Use Data Set:  <br/>
<img src="https://github.com/ShakeebTahir/ArcGIS-Python-Automation/assets/32227140/c53cf114-1955-45aa-994e-d3984aa80b34" height="80%" width="80%"/>
<br />
<br />
Make sure tool script reference is set correctly when loaded in:  <br/>
<img src="https://github.com/ShakeebTahir/ArcGIS-Python-Automation/assets/32227140/5e602911-b754-4399-9e8f-f7ccf2275c2d" height="80%" width="80%"/>
<br />
<br />
Add data sets into the tool:  <br/>
<img src="https://github.com/ShakeebTahir/ArcGIS-Python-Automation/assets/32227140/287e1150-03d6-4689-8205-4199bd3bda63"/>
<br />
<br />
Running the tool gives provides us with the most suitable areas to re-locate Bobcats:
<br/>
<img src="https://github.com/ShakeebTahir/ArcGIS-Python-Automation/assets/32227140/c99d1239-45ad-4227-b5d1-d073d5622b1c" height="80%" width="80%"/>
<br />
<b>Note: </b> Can edit the script to give more or less regions depending on needs by changing the "number_of_regions" input parameter in the "LocateRegions" function on Line 93
<br />

</p>
