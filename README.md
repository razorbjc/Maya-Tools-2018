# Maya Tools 2018
<b>HOW TO USE</b>
<br>These are a collection of Maya Modeling Tools I have written over the years. To use a script, just copy and paste all the text into Maya's script editor (Python Tab). Then execute by hightlighting all and pressing 'Alt+Enter'. Or you could make a shelf button by highlighting all, then middle mouse dragging to the shelf. Easy!
<br><br><br>
<b>camClipToggle.py</b>
<br>Increases the clipping plane range of all cameras in the scene to 10cm - 1,000,000cm. Clicking again will toggle all cameras back to default range. Good for working on environments without needing to manually edit clipping plane values.

<b>curveTube.py</b>
<br>If given a curve, the script will generate a tube with spans at the curve's CVs. If given tube geometry, it will instead create a curve with CVs at the center of each edge ring.

<b>dualToggle.py</b>
<br>When given two selectioned objects, dualToggle will hide one object and show the other. Then will switch their visibilities when run again. For quick, easy comparison between two models. Good for matching scans.

<b>faceCut.py</b>
<br>Given a complete edge loop or enclosure of edges, this script will select all faces within the edge perimeter.

<b>headCut.py</b>
<br>Selected faces or vertices will be ordered to have the first vertex IDs. Used for reordering character models so that the head consists of the first vertIDs.

<b>holeGrid.py</b>
<br>This script will fill a selected hole with grid geo. After the script is run, the grid verts are selected for further averaging. The 'offset' attribute in the channel box can be adjusted to fine-tune the rotation.

<b>imagePlaneToggle.py</b>
<br>Toggles imageplane visibility of current camera from 0% to 50% to 100%. Meant to be keybinded to quickly change the alpha of an imageplane without using the slider in the camera's attributes.

<b>removeNamespaces.py</b>
<br>Removes all namespaces. May need to be run multiple times for stacked namespaces

<b>replaceTopo.py</b>
<br>Replaces all objects of a certain topology with new geo(even if the object transforms have been lost/frozen). Good for updating many low-res trees, rocks, or woodplanks with high-res versions in environments.
<br> 1. Define an 'Old Mesh' which will be an example of the object/topology you want to replace.
<br> 2. Define a "New Mesh, which is what you want to replace the old meshes with. Should overlap in space with the 'Old Mesh"
<br> 3. Define which target objects you want to replace, then hit 'Run'

<b>smartCombine.py</b>
<br>Will combine objects while retaining the pivot, name, hierarchy, and display layer of the last selected object. History is deleted.

<b>smartExtract.py</b>
<br>Meant to be a cleaner alternative for Maya's Extract. If objects with separate meshes are selected, smartExtract will separate them. If given a face selection, smartExtract will extract faces but retain the name and pivot of the base geometry. The extracted pieces will be named/numbered and pivots centered.
<br>if given a completed edge loop, smartExtract will run faceCut and then extract faces.

<b>smartDuplicate.py</b>
<br>Meant to be a cleaner alternative for Maya's Duplicate. Duplicated faces will have centered pivots and clean names. if given a completed edge loop, smartDuplicate will run faceCut and then duplicate faces.

<b>unsmooth.py</b>
<br>Unsmooths geometry that has been smoothed, even without history. Kind of like zBrush's 'Reconstruct SubDivision Levels". Works on quad-only geo that has not been edited since the smoothing. For singular meshes only and can be very slow for meshes with 10k+ polygons. Maintains UVs.

<b>uvui.py</b>
<br>A custom UV toolset that allows access to the most commonly used tools. Includes better support for flipping UVs within the UDIM.

<b>versionUp.py</b>
<br>Shorcut for incrementally saving current scene while maintaining the number padding/convention.
