import typing

from abaqusConstants import *
from .AutoColors import AutoColors
from .Color import Color
from .Drawing import Drawing
from .Image import Image
from .JournalOptions import JournalOptions
from .MemoryReductionOptions import MemoryReductionOptions
from .NetworkDatabaseConnector import NetworkDatabaseConnector
from ..Animation.AVIOptions import AVIOptions
from ..Animation.AnimationOptions import AnimationOptions
from ..Animation.ImageAnimation import ImageAnimation
from ..Animation.ImageAnimationOptions import ImageAnimationOptions
from ..Animation.Movie import Movie
from ..Animation.QuickTimeOptions import QuickTimeOptions
from ..Canvas.Canvas import Canvas
from ..Canvas.DrawingArea import DrawingArea
from ..Canvas.Viewport import Viewport
from ..CustomKernel.RepositorySupport import RepositorySupport
from ..DisplayGroup.DisplayGroup import DisplayGroup
from ..DisplayOptions.GraphicsInfo import GraphicsInfo
from ..DisplayOptions.GraphicsOptions import GraphicsOptions
from ..DisplayOptions.LightOptions import LightOptions
from ..DisplayOptions.ViewportAnnotationOptions import ViewportAnnotationOptions
from ..FieldReport.FieldReportOptions import FieldReportOptions
from ..FieldReport.FreeBodyReportOptions import FreeBodyReportOptions
from ..Job.Queue import Queue
from ..Mesh.MesherOptions import MesherOptions
from ..Odb.Odb import Odb
from ..Odb.ScratchOdb import ScratchOdb
from ..OdbDisplay.DefaultOdbDisplay import DefaultOdbDisplay
from ..OdbDisplay.ViewerOptions import ViewerOptions
from ..PathAndProbe.CurrentProbeValues import CurrentProbeValues
from ..PathAndProbe.FreeBody import FreeBody
from ..PathAndProbe.NodeQuery import NodeQuery
from ..PathAndProbe.Path import Path
from ..PathAndProbe.ProbeOptions import ProbeOptions
from ..PathAndProbe.ProbeReport import ProbeReport
from ..PathAndProbe.SelectedProbeValues import SelectedProbeValues
from ..PathAndProbe.Spectrum import Spectrum
from ..PathAndProbe.Stream import Stream
from ..PlotOptions.MdbData import MdbData
from ..PlotOptions.OdbData import OdbData
from ..PredefinedField.TiffOptions import TiffOptions
from ..Print.EpsOptions import EpsOptions
from ..Print.PageSetupOptions import PageSetupOptions
from ..Print.PngOptions import PngOptions
from ..Print.PrintOptions import PrintOptions
from ..Print.PsOptions import PsOptions
from ..Print.SvgOptions import SvgOptions
from ..Sketcher.ConstrainedSketchOptions.ConstrainedSketcherOptions import ConstrainedSketcherOptions
from ..UtilityAndView.View import View
from ..XY.Chart import Chart
from ..XY.DefaultChartOptions import DefaultChartOptions
from ..XY.DefaultPlot import DefaultPlot
from ..XY.XYCurve import XYCurve
from ..XY.XYData import XYData
from ..XY.XYPlot import XYPlot
from ..XY.XYReportOptions import XYReportOptions


class SessionBase:
    """The Session object has no constructor. Abaqus creates the *session* member when a
    session is started. 

    Attributes
    ----------
    attachedToGui: Boolean
        A Boolean specifying whether an Abaqus interactive session is running.
    replayInProgress: Boolean
        A Boolean specifying whether Abaqus is executing a replay file.
    kernelMemoryFootprint: float
        A Float specifying the memory usage value for the Abaqus/CAE kernel process in
        megabytes.
    kernelMemoryMaxFootprint: float
        A Float specifying the maximum value for the memory usage for the Abaqus/CAE kernel
        process in megabytes.
    kernelMemoryLimit: float
        A Float specifying the limit for the memory use for the Abaqus/CAE kernel process in
        megabytes.
    colors: dict[str, Color]
        A repository of :py:class:`~abaqus.Session.Color.Color` objects.
    journalOptions: JournalOptions
        A :py:class:`~abaqus.Session.JournalOptions.JournalOptions` object specifying how to record selection of geometry in the journal
        and replay files.
    memoryReductionOptions: MemoryReductionOptions
        A :py:class:`~abaqus.Session.MemoryReductionOptions.MemoryReductionOptions` object specifying options for running in reduced memory mode.
    nodeQuery: NodeQuery
        A :py:class:`~abaqus.PathAndProbe.NodeQuery.NodeQuery` object specifying nodes and their coordinates in a path.
    sketcherOptions: ConstrainedSketcherOptions
        A :py:class:`~abaqus.Sketcher.ConstrainedSketchOptions.ConstrainedSketcherOptions.ConstrainedSketcherOptions` object specifying common options for all sketches.
    viewerOptions: ViewerOptions
        A :py:class:`~abaqus.OdbDisplay.ViewerOptions.ViewerOptions` object.
    animationOptions: AnimationOptions
        An :py:class:`~abaqus.Animation.AnimationOptions.AnimationOptions` object.
    aviOptions: AVIOptions
        An :py:class:`~abaqus.Animation.AVIOptions.AVIOptions` object.
    imageAnimationOptions: ImageAnimationOptions
        An :py:class:`~abaqus.Animation.ImageAnimationOptions.ImageAnimationOptions` object.
    imageAnimation: ImageAnimation
        An :py:class:`~abaqus.Animation.ImageAnimation.ImageAnimation` object.
    quickTimeOptions: QuickTimeOptions
        A :py:class:`~abaqus.Animation.QuickTimeOptions.QuickTimeOptions` object.
    viewports: dict[str, Viewport]
        A repository of :py:class:`~abaqus.Canvas.Viewport.Viewport` objects.
    customData: RepositorySupport
        A :py:class:`~abaqus.CustomKernel.RepositorySupport.RepositorySupport` object.
    defaultFieldReportOptions: FieldReportOptions
        A :py:class:`~abaqus.FieldReport.FieldReportOptions.FieldReportOptions` object.
    defaultFreeBodyReportOptions: FreeBodyReportOptions
        A :py:class:`~abaqus.FieldReport.FreeBodyReportOptions.FreeBodyReportOptions` object.
    fieldReportOptions: FieldReportOptions
        A :py:class:`~abaqus.FieldReport.FieldReportOptions.FieldReportOptions` object.
    freeBodyReportOptions: FreeBodyReportOptions
        A :py:class:`~abaqus.FieldReport.FreeBodyReportOptions.FreeBodyReportOptions` object.
    odbs: dict[str, Odb]
        A repository of :py:class:`~abaqus.Odb.Odb.Odb` objects.
    scratchOdbs: dict[str, ScratchOdb]
        A repository of :py:class:`~abaqus.Odb.ScratchOdb.ScratchOdb` objects.
    defaultOdbDisplay: DefaultOdbDisplay
        A :py:class:`~abaqus.OdbDisplay.DefaultOdbDisplay.DefaultOdbDisplay` object.
    defaultPlot: DefaultPlot
        A :py:class:`~abaqus.XY.DefaultPlot.DefaultPlot` object.
    defaultChartOptions: DefaultChartOptions
        A :py:class:`~abaqus.XY.DefaultChartOptions.DefaultChartOptions` object.
    odbData: dict[str, OdbData]
        A repository of :py:class:`~abaqus.PlotOptions.OdbData.OdbData` objects.
    mdbData: dict[str, MdbData]
        A repository of :py:class:`~abaqus.PlotOptions.MdbData.MdbData` objects.
    paths: dict[str, Path]
        A repository of :py:class:`~abaqus.PathAndProbe.Path.Path` objects.
    freeBodies: dict[str, FreeBody]
        A repository of :py:class:`~abaqus.PathAndProbe.FreeBody.FreeBody` objects.
    streams: dict[str, Stream]
        A repository of :py:class:`~abaqus.PathAndProbe.Stream.Stream` objects.
    spectrums: dict[str, Spectrum]
        A repository of :py:class:`~abaqus.PathAndProbe.Spectrum.Spectrum` objects.
    currentProbeValues: CurrentProbeValues
        A :py:class:`~abaqus.PathAndProbe.CurrentProbeValues.CurrentProbeValues` object.
    defaultProbeOptions: ProbeOptions
        A :py:class:`~abaqus.PathAndProbe.ProbeOptions.ProbeOptions` object.
    probeOptions: ProbeOptions
        A :py:class:`~abaqus.PathAndProbe.ProbeOptions.ProbeOptions` object.
    probeReport: ProbeReport
        A :py:class:`~abaqus.PathAndProbe.ProbeReport.ProbeReport` object.
    defaultProbeReport: ProbeReport
        A :py:class:`~abaqus.PathAndProbe.ProbeReport.ProbeReport` object.
    selectedProbeValues: SelectedProbeValues
        A :py:class:`~abaqus.PathAndProbe.SelectedProbeValues.SelectedProbeValues` object.
    printOptions: PrintOptions
        A :py:class:`~abaqus.Print.PrintOptions.PrintOptions` object.
    epsOptions: EpsOptions
        An :py:class:`~abaqus.Print.EpsOptions.EpsOptions` object.
    pageSetupOptions: PageSetupOptions
        A :py:class:`~abaqus.Print.PageSetupOptions.PageSetupOptions` object.
    pngOptions: PngOptions
        A :py:class:`~abaqus.Print.PngOptions.PngOptions` object.
    psOptions: PsOptions
        A :py:class:`~abaqus.Print.PsOptions.PsOptions` object.
    svgOptions: SvgOptions
        A :py:class:`~abaqus.Print.SvgOptions.SvgOptions` object.
    tiffOptions: TiffOptions
        A :py:class:`~abaqus.PredefinedField.TiffOptions.TiffOptions` object.
    autoColors: AutoColors
        An :py:class:`~abaqus.Session.AutoColors.AutoColors` object specifying the color palette to be used for color coding.
    xyColors: AutoColors
        An :py:class:`~abaqus.Session.AutoColors.AutoColors` object specifying the color palette to be used :py:class:`~.forXYCurve` objects.
    xyDataObjects: dict[str, XYData]
        A repository of :py:class:`~abaqus.XY.XYData.XYData` objects.
    curves: dict[str, XYCurve]
        A repository of :py:class:`~abaqus.XY.XYCurve.XYCurve` objects.
    xyPlots: dict[str, XYPlot]
        A repository of :py:class:`~abaqus.XY.XYPlot.XYPlot` objects.
    charts: dict[str, Chart]
        A repository of :py:class:`~abaqus.XY.Chart.Chart` objects.
    defaultXYReportOptions: XYReportOptions
        An :py:class:`~abaqus.XY.XYReportOptions.XYReportOptions` object.
    xyReportOptions: XYReportOptions
        An :py:class:`~abaqus.XY.XYReportOptions.XYReportOptions` object.
    views: dict[str, View]
        A repository of :py:class:`~abaqus.UtilityAndView.View.View` objects.
    networkDatabaseConnectors: dict[str, NetworkDatabaseConnector]
        A repository of :py:class:`~abaqus.Session.NetworkDatabaseConnector.NetworkDatabaseConnector` objects.
    displayGroups: dict[str, DisplayGroup]
        A repository of :py:class:`~abaqus.DisplayGroup.DisplayGroup.DisplayGroup` objects.
    graphicsInfo: GraphicsInfo
        A :py:class:`~abaqus.DisplayOptions.GraphicsInfo.GraphicsInfo` object.
    defaultGraphicsOptions: GraphicsOptions
        A :py:class:`~abaqus.DisplayOptions.GraphicsOptions.GraphicsOptions` object.
    graphicsOptions: GraphicsOptions
        A :py:class:`~abaqus.DisplayOptions.GraphicsOptions.GraphicsOptions` object.
    defaultViewportAnnotationOptions: ViewportAnnotationOptions
        A :py:class:`~abaqus.DisplayOptions.ViewportAnnotationOptions.ViewportAnnotationOptions` object.
    queues: dict[str, Queue]
        A repository of :py:class:`~abaqus.Job.Queue.Queue` objects.
    currentViewportName: str
        A String specifying the name of the current viewport.
    sessionState: dict
        A :py:class:`~.Dictionary` object specifying the viewports and their associated models. The :py:class:`~.Dictionary`
        key specifies the viewport name. The :py:class:`~.Dictionary` value is a :py:class:`~.Dictionary` specifying the
        model name.
    images: dict[str, Image]
        A repository of :py:class:`~abaqus.Session.Image.Image` objects.
    movies: dict[str, Movie]
        A repository of :py:class:`~abaqus.Animation.Movie.Movie` objects.
    defaultLightOptions: LightOptions
        A :py:class:`~abaqus.DisplayOptions.LightOptions.LightOptions` object.
    drawingArea: DrawingArea
        A :py:class:`~abaqus.Canvas.DrawingArea.DrawingArea` object.
    defaultMesherOptions: MesherOptions
        A :py:class:`~abaqus.Mesh.MesherOptions.MesherOptions` object specifying how to control default settings in the Mesh module.
    drawings: dict[str, Drawing]
        A repository of :py:class:`~abaqus.Session.Drawing.Drawing` objects.

    Notes
    -----
    This object can be accessed by:

    .. code-block:: python
    
        session

    """

    # A Boolean specifying whether an Abaqus interactive session is running. 
    attachedToGui: Boolean = OFF

    # A Boolean specifying whether Abaqus is executing a replay file. 
    replayInProgress: Boolean = OFF

    # A Float specifying the memory usage value for the Abaqus/CAE kernel process in 
    # megabytes. 
    kernelMemoryFootprint: float = None

    # A Float specifying the maximum value for the memory usage for the Abaqus/CAE kernel 
    # process in megabytes. 
    kernelMemoryMaxFootprint: float = None

    # A Float specifying the limit for the memory use for the Abaqus/CAE kernel process in 
    # megabytes. 
    kernelMemoryLimit: float = None

    # A repository of Color objects. 
    colors: dict[str, Color] = dict[str, Color]()

    # A JournalOptions object specifying how to record selection of geometry in the journal 
    # and replay files. 
    journalOptions: JournalOptions = JournalOptions()

    # A MemoryReductionOptions object specifying options for running in reduced memory mode. 
    memoryReductionOptions: MemoryReductionOptions = MemoryReductionOptions()

    # A NodeQuery object specifying nodes and their coordinates in a path. 
    nodeQuery: NodeQuery = NodeQuery()

    # A ConstrainedSketcherOptions object specifying common options for all sketches. 
    sketcherOptions: ConstrainedSketcherOptions = ConstrainedSketcherOptions()

    # A ViewerOptions object. 
    viewerOptions: ViewerOptions = ViewerOptions()

    # An AnimationOptions object. 
    animationOptions: AnimationOptions = AnimationOptions()

    # An AVIOptions object. 
    aviOptions: AVIOptions = AVIOptions()

    # An ImageAnimationOptions object. 
    imageAnimationOptions: ImageAnimationOptions = ImageAnimationOptions()

    # An ImageAnimation object. 
    imageAnimation: ImageAnimation = ImageAnimation('img', AVI)

    # A QuickTimeOptions object. 
    quickTimeOptions: QuickTimeOptions = QuickTimeOptions()

    # A repository of Viewport objects. 
    viewports: dict[str, Viewport] = dict[str, Viewport]()

    # A RepositorySupport object. 
    customData: RepositorySupport = RepositorySupport()

    # A FieldReportOptions object. 
    defaultFieldReportOptions: FieldReportOptions = FieldReportOptions()

    # A FreeBodyReportOptions object. 
    defaultFreeBodyReportOptions: FreeBodyReportOptions = FreeBodyReportOptions()

    # A FieldReportOptions object. 
    fieldReportOptions: FieldReportOptions = FieldReportOptions()

    # A FreeBodyReportOptions object. 
    freeBodyReportOptions: FreeBodyReportOptions = FreeBodyReportOptions()

    # A repository of Odb objects. 
    odbs: dict[str, Odb] = dict[str, Odb]()

    # A repository of ScratchOdb objects. 
    scratchOdbs: dict[str, ScratchOdb] = dict[str, ScratchOdb]()

    # A DefaultOdbDisplay object. 
    defaultOdbDisplay: DefaultOdbDisplay = DefaultOdbDisplay()

    # A DefaultPlot object. 
    defaultPlot: DefaultPlot = DefaultPlot()

    # A DefaultChartOptions object. 
    defaultChartOptions: DefaultChartOptions = DefaultChartOptions()

    # A repository of OdbData objects. 
    odbData: dict[str, OdbData] = dict[str, OdbData]()

    # A repository of MdbData objects. 
    mdbData: dict[str, MdbData] = dict[str, MdbData]()

    # A repository of Path objects. 
    paths: dict[str, Path] = dict[str, Path]()

    # A repository of FreeBody objects. 
    freeBodies: dict[str, FreeBody] = dict[str, FreeBody]()

    # A repository of Stream objects. 
    streams: dict[str, Stream] = dict[str, Stream]()

    # A repository of Spectrum objects. 
    spectrums: dict[str, Spectrum] = dict[str, Spectrum]()

    # A CurrentProbeValues object. 
    currentProbeValues: CurrentProbeValues = CurrentProbeValues()

    # A ProbeOptions object. 
    defaultProbeOptions: ProbeOptions = ProbeOptions()

    # A ProbeOptions object. 
    probeOptions: ProbeOptions = ProbeOptions()

    # A ProbeReport object. 
    probeReport: ProbeReport = ProbeReport()

    # A ProbeReport object. 
    defaultProbeReport: ProbeReport = ProbeReport()

    # A SelectedProbeValues object. 
    selectedProbeValues: SelectedProbeValues = SelectedProbeValues()

    # A PrintOptions object. 
    printOptions: PrintOptions = PrintOptions()

    # An EpsOptions object. 
    epsOptions: EpsOptions = EpsOptions()

    # A PageSetupOptions object. 
    pageSetupOptions: PageSetupOptions = PageSetupOptions()

    # A PngOptions object. 
    pngOptions: PngOptions = PngOptions()

    # A PsOptions object. 
    psOptions: PsOptions = PsOptions()

    # A SvgOptions object. 
    svgOptions: SvgOptions = SvgOptions()

    # A TiffOptions object. 
    tiffOptions: TiffOptions = TiffOptions()

    # An AutoColors object specifying the color palette to be used for color coding. 
    autoColors: AutoColors = AutoColors()

    # An AutoColors object specifying the color palette to be used forXYCurve objects. 
    xyColors: AutoColors = AutoColors()

    # A repository of XYData objects. 
    xyDataObjects: dict[str, XYData] = dict[str, XYData]()

    # A repository of XYCurve objects. 
    curves: dict[str, XYCurve] = dict[str, XYCurve]()

    # A repository of XYPlot objects. 
    xyPlots: dict[str, XYPlot] = dict[str, XYPlot]()

    # A repository of Chart objects. 
    charts: dict[str, Chart] = dict[str, Chart]()

    # An XYReportOptions object. 
    defaultXYReportOptions: XYReportOptions = XYReportOptions()

    # An XYReportOptions object. 
    xyReportOptions: XYReportOptions = XYReportOptions()

    # A repository of View objects. 
    views: dict[str, View] = dict[str, View]()

    # A repository of NetworkDatabaseConnector objects. 
    networkDatabaseConnectors: dict[str, NetworkDatabaseConnector] = dict[str, NetworkDatabaseConnector]()

    # A repository of DisplayGroup objects. 
    displayGroups: dict[str, DisplayGroup] = dict[str, DisplayGroup]()

    # A GraphicsInfo object. 
    graphicsInfo: GraphicsInfo = GraphicsInfo()

    # A GraphicsOptions object. 
    defaultGraphicsOptions: GraphicsOptions = GraphicsOptions()

    # A GraphicsOptions object. 
    graphicsOptions: GraphicsOptions = GraphicsOptions()

    # A ViewportAnnotationOptions object. 
    defaultViewportAnnotationOptions: ViewportAnnotationOptions = ViewportAnnotationOptions()

    # A repository of Queue objects. 
    queues: dict[str, Queue] = dict[str, Queue]()

    # A String specifying the name of the current viewport. 
    currentViewportName: str = ''

    # A Dictionary object specifying the viewports and their associated models. The Dictionary 
    # key specifies the viewport name. The Dictionary value is a Dictionary specifying the 
    # model name. 
    sessionState: dict = None

    # A repository of Image objects. 
    images: dict[str, Image] = dict[str, Image]()

    # A repository of Movie objects. 
    movies: dict[str, Movie] = dict[str, Movie]()

    # A LightOptions object. 
    defaultLightOptions: LightOptions = LightOptions()

    # A DrawingArea object. 
    drawingArea: DrawingArea = DrawingArea()

    # A MesherOptions object specifying how to control default settings in the Mesh module. 
    defaultMesherOptions: MesherOptions = MesherOptions()

    # A repository of Drawing objects. 
    drawings: dict[str, Drawing] = dict[str, Drawing]()

    def setValues(self, kernelMemoryLimit: float = None):
        """This method modifies the Session object.
        
        Parameters
        ----------
        kernelMemoryLimit
            A Float specifying the memory limit value for the Abaqus/CAE kernel process in 
            megabytes. If the limit is exceeded, Abaqus/CAE displays an error message.The default 
            memory limit value for Windows 32-bit systems if not set is 1800 MB. Increasing the 
            memory limit is not recommended unless you are using a Windows 32-bit system with the 
            boot option /3GB /userva=SizeInMBytes to extend the amount of memory available for 
            Abaqus/CAE. In this case the limit can be changed to 2800 MB.If the kernel memory size 
            reaches the **abq_ker_memory** value or the virtual memory limit of the machine, the 
            following message will be displayed:`Operation did not complete due to a memory 
            allocation failure.`For optimal performance, the memory limit should be set to a value 
            less than the physical amount of memory on the machine.The minimum setting allowed is 
            256 MB. 
        """
        pass

    def enableCADConnection(self, CADName: str, portNum: int = None):
        """This method enables the Abaqus/CAE listening port for the specified *CAD* system.
        
        Parameters
        ----------
        CADName
            A String specifying the CAD system. Available options are Pro/ENGINEER, CATIA V5, CATIA 
            V6, NX and SolidWorks. 
        portNum
            An Integer specifying the port number to be used by the CAD system to communicate with 
            Abaqus/CAE. If unspecified, attempts will be made to identify an open port. The default 
            ports used are as follow:Pro/E : 49178CATIA V5 : 49179SolidWorks : 49180NX : 49181CATIA 
            V6 : 49182 

        Returns
        -------
            The connection port number used for the CAD connection.
        """
        pass

    def isCADConnectionEnabled(self):
        """This method checks the status of CAD Connection.

        Returns
        -------
            A Boolean value of True if the CAD connection enabled and False if the CAD connection 
            disabled.
        """
        pass

    def disableCADConnection(self, CADName: str):
        """This method disables an associative import CAD connection that was enabled.
        
        Parameters
        ----------
        CADName
            A String specifying the CAD system for which associative import will be disabled. 
            Available options are Pro/ENGINEER, CATIA V5, and CATIA V6, NX and SolidWorks. 
        """
        pass

    def enableParameterUpdate(self, CADName: str, CADVersion: str, CADPort: int = None):
        """This method enables parameter updates for ProE and NX by establishing a connection with
        the listening port previously setup by the CAD application.
        
        Parameters
        ----------
        CADName
            A String specifying the CAD system for which parameter update will be enabled. Available 
            options are Pro/ENGINEER and NX. 
        CADVersion
            A String specifying the CAD system version. Allowable options take the form of the 
            specific CAD system plus a version string. Examples for Pro/ENGINEER are "Wildfire5" and 
            "Creo4." An NX example is "NX11." 
        CADPort
            An Integer specifying the port number to be used by Abaqus/CAE to communicate with the 
            CAD system. If unspecified, attempts will be made to identify an open port. This port 
            number is not the same as the *portNum* used by the associative import interface. The 
            default CAD listening ports are as follow:ProE : 3344NX : 3344 
        """
        pass

    def setCADPortNumber(self, CADName: str, Port: str):
        """This method enables parameter updates for CATIA V5 and CATIA V6 by establishing a
        connection with the listening port previously setup by the CAD application. This port
        number is used to send the parameter information to the CAD system.
        
        Parameters
        ----------
        CADName
            A String specifying the CAD system for which the port number will be saved. The 
            available options are 'CATIA V5' and ' CATIA V6'. 
        Port
            An integer specifying the port number to be used by Abaqus/CAE to send the modified 
            parameters to the CAD system. 
        """
        pass

    def updateCADParameters(self, modelName: str, CADName: str, parameterFile: str, CADPartFile: str,
                            CADPartName: str = ''):
        """This method updates the parameters for the specified model using the specified parameter
        file.
        
        Parameters
        ----------
        modelName
            A String specifying the model name to update. 
        CADName
            A String specifying the CAD system for which Abaqus updates the parameters. The 
            available options are 'Pro/ENGINEER', 'CATIA V5' and 'CATIA V6'. 
        parameterFile
            A parameter file containing the parameters that were exposed in the CAD system using the 
            'ABQ_' prefix. 
        CADPartFile
            A file name specifying the CAD part file for which parameter update is triggered.For 
            *CADName*='CATIA V5' or 'CATIA V6', you can specify either products or parts using this 
            argument. If you specify a product, Abaqus updates all of the parts associated with that 
            product.For *CADName*='Pro/ENGINEER', this argument is optional, and you can specify 
            update for parts only. However, a single file can be associated with multiple parts in 
            the case of family tables. In this case, Abaqus updates all listed parts. 
        CADPartName
            An String specifying the part name to update. This part name should match the part name 
            in the originating CAD system.If you specify neither *CADPartFile* nor *CADPartName* 
            during an update in which you specified *CADName*='Pro/ENGINEER', Abaqus updates all of 
            the parts in the specified file. 
        """
        pass

    def disableParameterUpdate(self, CADName: str):
        """This method disables an associative CAD connection using parameters.
        
        Parameters
        ----------
        CADName
            A String specifying the CAD system for which the parameter update will be disabled. 
            Available option is Pro/ENGINEER. 
        """
        pass

    def printToFile(self, fileName: str, format: SymbolicConstant = PNG, canvasObjects: tuple[Canvas] = (),
                    compression: Boolean = OFF):
        """This method prints canvas objects to a file using the attributes stored in the
        PrintOptions object and the appropriate format options object.
        
        Parameters
        ----------
        fileName
            A String specifying the file to which the image is to be written. If no file extension 
            is supplied, an extension is added based on the selected image format (.ps, .eps, .png, 
            .tif, .svg, or .svgz). 
        format
            A SymbolicConstant specifying the image format. Possible values are PNG, SVG, TIFF, PS, 
            and EPS. The default value is PNG. 
        canvasObjects
            A sequence of canvas objects (viewports, text strings, or arrows) to print. The default 
            is to print all canvas objects. 
        compression
            A Boolean specifying the format for an SVG file. It is only valid to use this argument 
            when *format* is SVG. Possible values are False (Uncompressed) and True (Compressed). 
        """
        pass

    def printToPrinter(self, printCommand: str = '', numCopies: int = 1, canvasObjects: tuple[Canvas] = ()):
        """This method prints canvas objects to a Windows printer or to a PostScript printer. The
        attributes used for printing to a Windows printer are stored in the PrintOptions object
        and the PageSetupOptions object; the attributes used for printing to a PostScript
        printer are stored in the PrintOptions object and the PsOptions object.
        
        Parameters
        ----------
        printCommand
            A String specifying the operating system command or printer name to issue for printing 
            to the printer. The default value is “lpr” or the value specified by the printOptions 
            method. If you create a script to print directly to a Windows printer, the 
            *printCommand* must take the following 
            form:
            `session.printToPrinter.setValues(printCommand='PRINTER[number of characters in name]:printername PROPERTIES[number of characters in properties]:document properties')`
            The `PROPERTIES` is a list of characters that represents the 
            printing preferences for the selected Windows printer. The properties are not required 
            in a script; the printed output will use the current settings for the selected printer. 
            You can use `'PRINTER[7]: DEFAULT'` to specify the default Windows printer. 
        numCopies
            An Int specifying the number of copies to print. Possible values are 1 ≤≤ *numCopies* ≤≤ 
            100. The default value is 1. 
        canvasObjects
            A sequence of canvas objects (viewports, text strings, or arrows) to print. The default 
            is to print all canvas objects.

        Raises
        ------
            - If *printCommand* is invalid: 
              SystemError: invalid print command 
            - If the print command fails: 
              SystemError: print command failed 
            - If *numCopies* is out of range: 
              RangeError: numCopies must be in the range 1 <= value <= 100 
            - If *compression* is specified when *format* is not SVG : 
              TypeError: keyword error on compression 
        """
        pass

    def saveOptions(self, directory: SymbolicConstant):
        """This method saves your customized display settings.
        
        Parameters
        ----------
        directory
            A SymbolicConstant specifying the directory in which Abaqus saves the file that will be 
            used to restore your customized settings (abaqus_2021.gpr). Possible values are HOME and 
            CURRENT. 
        """
        pass

    def writeVrmlFile(self, fileName: str, format: Boolean = OFF, canvasObjects: tuple[Canvas] = ()):
        """This method exports the current viewport objects to a file.
        
        Parameters
        ----------
        fileName
            A String specifying the file to which the graphics data is to be written. If no file 
            extension is supplied, an extension is added based on the selected format (.wrl, .wrz). 
        format
            A Boolean specifying the format. Possible values are False (Uncompressed) and True 
            (Compressed). 
        canvasObjects
            A sequence of canvas objects (viewports, text strings, or arrows) to export. 
        """
        pass

    def write3DXMLFile(self, fileName: str, format: Boolean = OFF, canvasObjects: tuple[Canvas] = ()):
        """This method exports the current viewport objects to a file.
        
        Parameters
        ----------
        fileName
            A String specifying the file to which the graphics data is to be written. If no file 
            extension is supplied, (.3dxml) will be added. 
        format
            A Boolean specifying the format. Possible values are False (Uncompressed) and True 
            (Compressed). 
        canvasObjects
            A sequence of canvas objects to export. 
        """
        pass

    def writeOBJFile(self, fileName: str, canvasObjects: tuple[Canvas] = ()):
        """This method exports the current viewport objects to a file.
        
        Parameters
        ----------
        fileName
            A String specifying the file to which the graphics data is to be written. If no file 
            extension is supplied, (.obj) will be added. 
        canvasObjects
            A sequence of canvas objects to export. 
        """
        pass

    @typing.overload
    def openOdb(self, path: str, readOnly: Boolean = OFF, readInternalSets: Boolean = OFF) -> Odb:
        """This method opens an existing output database (.odb) file and creates a new Odb object.
        You typically execute this method outside Abaqus/CAE when, in most cases, only one
        output database is open at any time. For example
        import odbAccess
        shockLoadOdb = odbAccess.openOdb(path='myOdb.odb')
        
        Parameters
        ----------
        path
            A String specifying the path to an existing output database (.odb) file.
        readOnly
            A Boolean specifying whether the file will permit only read access or both read and
            write access. The initial value is False, indicating that both read and write access
            will be permitted.
        readInternalSets
            A Boolean specifying whether the file will permit access to sets specified as Internal
            on the database. The initial value is False, indicating that internal sets will not be
            read.

        Returns
        -------
            An Odb object.

        Raises
        ------
            - If the output database was generated by a previous release of Abaqus and needs
            upgrading:
              OdbError: The database is from a previous release of Abaqus. Run `abaqus upgrade -job
            <newFilename> -odb <oldFileName>` to upgrade it.
            - If the output database was generated by a newer release of Abaqus, and the
            installation of Abaqus needs upgrading:
              OdbError: Abaqus installation must be upgraded before this output database can be
            opened.
        """
        pass

    @typing.overload
    def openOdb(self, name: str, path: str = '', readOnly: Boolean = OFF) -> Odb:
        """This method opens an existing output database (.odb) file and creates a new Odb object.
        This method is accessed only via the session object inside Abaqus/CAE and adds the new
        Odb object to the session.odbs repository. This method allows you to open multiple
        output databases at the same time and to use the repository key to specify a particular
        output database. For example
        import visualization
        session.openOdb(name='myOdb', path='stress.odb', readOnly=True)
        
        Parameters
        ----------
        name
            A String specifying the repository key. If the*name* is not the same as the*path* to the
            output database (.odb) file, the *path* must be specified as well. Additionally, to
            support backwards compatibility of the interface, if the *name* parameter is omitted,
            the *path* and *name* will be presumed to be the same.
        path
            A String specifying the path to an existing output database (.odb) file.
        readOnly
            A Boolean specifying whether the file will permit only read access or both read and
            write access. The initial value is TRUE when the output database file is opened from
            Abaqus/CAE, indicating that only read access will be permitted.

        Returns
        -------
            An Odb object.

        Raises
        ------
            - If the output database was generated by a previous release of Abaqus and needs
            upgrading:
              OdbError: The database is from a previous release of Abaqus.Run `abaqus upgrade -job
            <newFilename> -odb <oldFileName>` to upgrade it.
            - If the output database was generated by a newer release of Abaqus, and the
            installation of Abaqus needs upgrading:
              OdbError: Abaqus installation must be upgraded before this output database can be
            opened.
            - If the file is not a valid database:
              AbaqusError: Cannot open file <*filename*>.
        """
        pass

    def openOdb(self, name: str, *args, **kwargs) -> Odb:
        """This method opens an existing output database (.odb) file and creates a new Odb object.
        You typically execute this method outside Abaqus/CAE when, in most cases, only one
        output database is open at any time. For example
        import odbAccess
        shockLoadOdb = odbAccess.openOdb(path='myOdb.odb')
        
        Parameters
        ----------
        name
            A String specifying the repository key. If the*name* is not the same as the*path* to the
            output database (.odb) file, the *path* must be specified as well. Additionally, to
            support backwards compatibility of the interface, if the *name* parameter is omitted,
            the *path* and *name* will be presumed to be the same.

        Returns
        -------
            An Odb object.

        Raises
        ------
            - If the output database was generated by a previous release of Abaqus and needs
            upgrading:
              OdbError: The database is from a previous release of Abaqus. Run `abaqus upgrade -job
            <newFilename> -odb <oldFileName>` to upgrade it.
            - If the output database was generated by a newer release of Abaqus, and the
            installation of Abaqus needs upgrading:
              OdbError: Abaqus installation must be upgraded before this output database can be
            opened.
        """
        self.odbs[name] = odb = Odb(name, *args, **kwargs)
        return odb

    @staticmethod
    def exit():
        os.system('exit')
