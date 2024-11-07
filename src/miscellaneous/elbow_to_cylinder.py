# Python Script, API Version = V241
# type: ignore
# ruff: noqa: F821

# Get the torus body of the selected surface. If the torus is
# connected to the pipes: split the body.
def getTorusfromSur(sel):
    torus = sel.Items[0] # torus is a surface
    cyls = []
    edgs = []
    # If there are cylinders attached to the elbow: store the
    # cylinder surfaces and store the edges that divide the 
    # elbow from the cylinder. The edges will be used to cut
    # the elbow.
    for edg in torus.Edges:
        for f in edg.Faces:
            if f.Shape.Geometry.GetType() == Cylinder:
                cyls.append(f)
                edgs.append((edg.Shape.Geometry.Axis.Direction,edg))
    if cyls:
        edgs = sorted(edgs) # Sort edges according to their axis dir.
        edgs =[edgs[0][1],edgs[-1][1]] # Obtain two edgs with different dir.
        planelist = []
        for edg in edgs: # Split the torus.
            bod = torus.Parent
            selection = Selection.Create(bod)
            datum = Selection.Create(edg)
            SplitBody.Execute(selection, datum)  
    
    # Sets the torus body active so the MovetoNew function will be able
    # to copy and delete it.
    bod = torus.Parent
    Selection.Create(bod).SetActive() 
    return cyls

# Copies the torus body, deletes it and pastes it into a new design.
# It also returns the list of the connected outer cylinders if any
# and the place of the Structure Tree where the component is located.    
def MovetoNew():
    sel = Selection.GetActive()
    originalComp = sel.Items[0].Parent.Parent.Parent
    cyls = getTorusfromSur(sel)
    sel = Selection.GetActive()
    Copy.ToClipboard(sel)
    Delete.Execute(sel)
    DocumentHelper.CreateNewDocument()
    Paste.FromClipboard()
    return cyls,originalComp

# Get the inner radius of the only body in the design and the thickness if apply,
# if not the thickness value will be zero.
def getradius():
    body = GetRootPart().Bodies[0]
    # Ensures that the number of edges will be 2 if solid and 4 if hollow
    FixSplitEdges.FindAndFix() 
    if body.Edges.Count == 2:
        rad = body.Edges[0].Shape.GetGeometry[Circle]().Radius
        # convert rad to mm
        rad = rad *1000
        thick = 0
    if body.Edges.Count > 2:
        rad1 = body.Edges[0].Shape.GetGeometry[Circle]().Radius
        for i in  body.Edges:
            if  i.Shape.GetGeometry[Circle]().Radius != rad1:
                rad2 = i.Shape.GetGeometry[Circle]().Radius
                break
        # convert rad to mm
        rad1 = rad1*1000
        rad2 = rad2*1000
        thick = abs(rad1-rad2)
        if rad1 > rad2:
            rad = rad2
        else:
            rad = rad1
    return rad,thick

# Create planes tangent to both ends of the torus
def getInitialEnds():
    body = GetRootPart().Bodies[0]
    listofplanes,torus,cyls = getplanes(body)
    for i in listofplanes:
        sel = Selection.Create(i)
        DatumPlaneCreator.Create(sel,True,None)
        
# Returns the faces of the body according to their type 
def getplanes(body):
    facelist = body.Faces
    planelist = []
    torus=[]
    cyls=[]
    for i in facelist:
        if i.Shape.Geometry.GetType() == Plane:
            planelist.append(i)
        if i.Shape.Geometry.GetType() == Cylinder:
            cyls.append(i)
        # If the surface is a spline will treat it as if it were a torus
        if i.Shape.Geometry.GetType() == Torus or i.Shape.Geometry.GetType() == ProceduralSurface:
            torus.append(i)
    return planelist,torus,cyls

# Divides the arc into n points and draw lines between them        
def drawlines(arc,n): 
    n = int(n)
    # First point of the list is the initial end of the arc.
    listofpoints=[arc.EvalProportion(0).Point] 
    for i in range(n):
        x = float(i+1)/n 
        listofpoints.append(arc.EvalProportion(x).Point)
    isConstruction = True
    for j in range(n):
        SketchLine.Create(listofpoints[j], listofpoints[j+1], isConstruction)
   
# Returns a list with all the straight lines of the model   
def getlines():
    curvelist = GetRootPart().Curves
    linelist = []
    for i in curvelist:
        if i.Shape.Geometry.GetType( ) == Line:
            linelist.append(i)
    return linelist
    
# Create cylinders of radius rad from the lines    
def createcyl(lines,rad): 
    selection = Selection.Create(lines)
    TubeBody.Create(selection, MM(rad), None)

# Eliminates the rounds between the cylinders by applying a fill
# operation to all the spherical surfaces. Must be in 3D mode to work.
def fill(): 
    for face in GetRootPart().Bodies[0].Faces:
        if face.Shape.Geometry.GetType() == Sphere:
            selection = Selection.Create(face)
            secondarySelection = Selection()
            options = FillOptions()
            result = Fill.Execute(selection, secondarySelection, options, FillMode.ThreeD, None)

# Extrude both ends of the only body in design
def extrudeEnds():
    body = GetRootPart().Bodies[0]
    listofplanes,torus,cyls = getplanes(body)
    for i in listofplanes:
        sel = Selection.Create(i)
        options = ExtrudeFaceOptions()
        options.ExtrudeType = ExtrudeType.Add
        result = ExtrudeFaces.Execute(sel, MM(50), options)

# If applies make a pipe of the proper thickness        
def createPipe2(thick):
   # Sometimes a solid pipe will give a thickness value as if it were 
   # hollow, being this value extremely small (1e-12 or less).  
   if thick > 1e-10:
       l,n,c = getplanes(GetRootPart().Bodies[0])
       selection = Selection.Create(l)
       result = Shell.RemoveFaces(selection, MM(thick))
   return

# Divides the object using the initial torus ends
def cutExtraEnds():
    selection = Selection.Create(GetRootPart().Bodies[0])
    datum = Selection.Create(GetRootPart().DatumPlanes)
    result = SplitBody.Execute(selection, datum)

# From the torus body create a sketch plane and project there 
# the arc representing its trajectory.    
def getarcfromtorus():
    # Get three points from torus and create a plane
    body = GetRootPart().Bodies[0]
    planelist,torus,cyls = getplanes(body)
    plane1 = planelist[0]
    plane2 = planelist[1]
    p1 =plane1.MidPoint().Point
    P1 = SketchPoint.Create(p1)
    p2 =plane2.MidPoint().Point
    P2 = SketchPoint.Create(p2)
    p3 = torus[0].MidPoint().Point
    P3 = SketchPoint.Create(p3)
    sel =Selection.Create([P1.CreatedCurves[0],P2.CreatedCurves[0],P3.CreatedCurves[0]])
    datp = DatumPlaneCreator.Create(sel, True, None)
    # Create the axis and project it to the sketch plane
    selection = Selection.Create(torus[0])
    axistorus = DatumLineCreator.Create(selection, False, None)
    selection = Selection.Create(axistorus.CreatedLine)
    plane = datp.CreatedPlanes[0].Shape.Geometry
    P4 = ProjectToSketch.Create(selection, plane)
    # Draw the arc
    origin = P4.CreatedCurves[0].Shape.EndPoint
    start = p2
    end = p1
    senseClockWise = False
    SketchArc.CreateSweepArc(origin, start, end, senseClockWise)
    # Delete non useful components
    Copy.ToClipboard(Selection.Create(GetRootPart().Curves[-1]))
    seldel = Selection.Create(GetRootPart().Curves)
    Delete.Execute(seldel)
    seldel = Selection.Create(GetRootPart().DatumPlanes)
    Delete.Execute(seldel)
    seldel = Selection.Create(GetRootPart().DatumLines)
    Delete.Execute(seldel)
    Paste.FromClipboard()

# Create new cylinders at the ends of the torus
def obtaincyls():
    bod = GetRootPart().Bodies[0]
    for f in bod.Faces:
        if f.Shape.Geometry.GetType() == Plane:
            sel = Selection.Create(f) 
            options = ExtrudeFaceOptions()
            ExtrudeFaces.Execute(sel, MM(500), options) 

# Deletes surfaces and makes use of the FixMissingFaces tool to recover solids.
# The result is that we obtain two solid body cyilinders ready to be extruded to
# get a corner.
def getsolidcyls():
    listofplanes,torus,cyls = getplanes(GetRootPart().Bodies[0])
    l=[]
    if len(cyls) > 2: # If the cylinders are pipes, delete also the inner cylinders and planes
        for c in cyls:
            l.append((c.Shape.Area,c))
        cyls = sorted(l)
        cyls = [cyls[0][1],cyls[1][1]]
        seldel = Selection.Create(torus+listofplanes+[cyls[0]]+[cyls[1]])
        Delete.Execute(seldel)
    else:
        seldel = Selection.Create(torus)
        Delete.Execute(seldel)
    options = FixMissingFacesOptions()
    FixMissingFaces.FindAndFix(options)
    options = FixMissingFacesOptions() # Run it again because sometimes it doesnt find all the faces the first time
    FixMissingFaces.FindAndFix(options)

# Generates the corner for the pipes and splits it at the original torus ends
def getCorner():
    for bod in GetRootPart().Bodies: # Extrude the correct end of the cylinder to an extremely long distance, this 
                                     # way we will know which surfaces should be removed (the bigger ones)
        selection = Selection.Create(bod.Faces[2]) 
        options = ExtrudeFaceOptions()
        options.ExtrudeType = ExtrudeType.ForceIndependent
        result = ExtrudeFaces.Execute(selection,(100), options)
    targets = Selection.Create(GetRootPart().Bodies[0], GetRootPart().Bodies[1])
    result = Combine.Merge(targets)
    flist = []
    for face in GetRootPart().Bodies[0].Faces:
        flist.append((face.Shape.Area,face))
    flist = sorted(flist)
    selection = Selection.Create([flist[-1][1],flist[-2][1]]) # Select the two biggest areas
    secondarySelection = Selection()
    options = FillOptions()
    Fill.Execute(selection, secondarySelection, options, FillMode.ThreeD, None)
    selection = Selection.Create(GetRootPart().Bodies[0])
    datum = Selection.Create(GetRootPart().DatumPlanes)
    result = SplitBody.Execute(selection, datum)

# Reduces the radius of the cylinders to fit the original inner radius of the pipe if applies    
def reduceCyl(thick):
    if thick > 1e-10:
       cyls = []
       for bod in GetRootPart().Bodies:
           for face in bod.Faces:
               if face.Shape.Geometry.GetType() == Cylinder:
                   cyls.append((face.Shape.Area,face))
       cyls = sorted(cyls)
       selection = Selection.Create(cyls[0][1],cyls[1][1])
       options = OffsetFaceOptions()
       options.OffsetMode = OffsetMode.MoveFacesTogether
       options.ExtrudeType = ExtrudeType.ForceIndependent
       result = OffsetFaces.Execute(selection, MM(-thick), Direction.Create(-0.7, 0.7, 0), options)

# Creates the hollow pipe if applies        
def createPipe1(thick):
    if thick > 1e-10:
        B = GetRootPart().Bodies[0]
        for bod in GetRootPart().Bodies: # Selects the smallest body (the corner)
            if bod.Shape.Volume < B.Shape.Volume:
                B = bod
        l,nothing,nothing2 = getplanes(B)
        selection = Selection.Create(l)
        result = Shell.RemoveFaces(selection, MM(thick))   

# Copy the resulting set of cylinders and pastes it to the original design
# while deleting the temporary design used.
def goback(originalComp):
    # Sometimes some minor bodies are created. Here we find the proper body as it
    # will be the smallest one to have two circular ends.
    bods = []
    for bod in GetRootPart().Bodies:
        trigg=0
        for edg in bod.Edges:
            if edg.Shape.Geometry.GetType() == Circle:
                trigg=trigg+1
        if trigg >1:
            bods.append((bod.Shape.Volume,bod))
    bod = sorted(bods)[0][1]
    Copy.ToClipboard(Selection.Create(bod))
    DocumentHelper.CloseDocument()
    if originalComp:
        ComponentHelper.SetActive(originalComp)
    result = Paste.FromClipboard()
    ComponentHelper.SetRootActive()
    return result

# Copy the resulting set of cylinders and pastes it to the original design
# while deleting the temporary design used.     
def backToOriginal(originalComp):
    B = GetRootPart().Bodies[0]
    for b in GetRootPart().Bodies: # Takes the body with more edges
        if b.Edges.Count > B.Edges.Count:
            B = b
    sel = Selection.Create(B)
    Copy.ToClipboard(sel)
    DocumentHelper.CloseDocument()
    if originalComp:
        ComponentHelper.SetActive(originalComp)
    result = Paste.FromClipboard()
    ComponentHelper.SetRootActive()
    return result

#------------------------------
#---------Parameters-----------
cylNum = Parameters.Parameter1

# ------- Execution -----------
if cylNum <= 1:
    # Execution of script for pipe prolongation
    cyls,originalComp = MovetoNew()
    rad,thick = getradius()
    getInitialEnds()
    obtaincyls()
    getsolidcyls()
    getCorner()
    reduceCyl(thick)
    createPipe1(thick)
    result = goback(originalComp)
    # Creates a plane to split the two resulting cylinders
    for edg in result.CreatedObjects[0].Edges:
        if edg.Shape.Geometry.GetType() == Ellipse:
            datum = Selection.Create(edg)
            break 
    # Merge the result with its connecting pipes and then splits it by the corner
    if cyls:
        targets = Selection.Create([cyls[0].Parent,result.CreatedObjects[0],cyls[-1].Parent])
        Combine.Merge(targets)
        selection = Selection.Create(cyls[0].Parent)
        SplitBody.Execute(selection, datum)

if cylNum > 1:
    # Execution of scipt for arc aprox.
    cyls,originalComp = MovetoNew()
    rad,thick = getradius()
    getarcfromtorus()
    getInitialEnds()
    arc = GetRootPart().Curves[0]
    drawlines(arc,cylNum)
    seldel = Selection.Create(GetRootPart().Curves[0]) # Delete the arc now that we have the lines
    Delete.Execute(seldel)
    lines = getlines()
    seldel = Selection.Create(GetRootPart().Bodies[0]) # Delete the torus body
    Delete.Execute(seldel)
    createcyl(lines,rad)
    
    mode = InteractionMode.Solid # Returns to 3D mode to use the fill command
    result = ViewHelper.SetViewMode(mode, None)
    
    fill()
    extrudeEnds()
    createPipe2(thick)
    cutExtraEnds()
    result = backToOriginal(originalComp)
    
    bod = result.CreatedObjects[0]
    # Finds the cylinder faces that are at both ends of the object
    endCyls = []
    for f in bod.Faces:
        if f.Shape.Geometry.GetType() == Cylinder:
            for ad in f.AdjacentFaces:
                if ad.Shape.Geometry.GetType() == Plane:
                    endCyls.append(f)
                    
    # Merge the resulting object with the initial pipes
    if cyls:
        targets = Selection.Create([cyls[0].Parent,result.CreatedObjects[0],cyls[-1].Parent])
        result = Combine.Merge(targets)
        
    # Find the planes connected to the resulting solid (there should not be anyone, all the 
    # solids should be cylinders)
    badPlanes = []
    for cyl in endCyls:
        for f in cyl.AdjacentFaces:
            if f.Shape.Geometry.GetType() == Plane:
                badPlanes.append(f)
                
    # Applies a fill operation to all the planes
    if badPlanes:
        selection = Selection.Create(badPlanes)    
        secondarySelection = Selection()
        options = FillOptions()
        result = Fill.Execute(selection, secondarySelection, options, FillMode.ThreeD)

print('Finished')
