from typing import Literal, List, Union, Any, Optional, Dict, Type
from dataclasses import dataclass, field
from fastclasses_json import dataclass_json, JSONMixin
from enum import Enum

def to_object(obj: Dict[str, Any]) -> Optional['AnyObject']:
    if obj is not None and '_class' in obj.keys() and (obj['_class'] in class_map.keys()):
        return class_map[obj['_class']].from_dict(obj)
    else:
        return None
Uuid = str

@dataclass_json
@dataclass
class AssetCollection(JSONMixin):
    class_: Literal['assetCollection'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    do_objectID: 'Uuid'
    colorAssets: List['ColorAsset']
    gradientAssets: List['GradientAsset']
    images: List[Union['FileRef', 'DataRef']]
    colors: List['Color']
    gradients: List['Gradient']
    exportPresets: List[Any]
    imageCollection: Optional['ImageCollection'] = None

@dataclass_json
@dataclass
class ImageCollection(JSONMixin):
    class_: Literal['imageCollection'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    images: Any

@dataclass_json
@dataclass
class ColorAsset(JSONMixin):
    class_: Literal['MSImmutableColorAsset'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    do_objectID: 'Uuid'
    name: str
    color: 'Color'

@dataclass_json
@dataclass
class Color(JSONMixin):
    class_: Literal['color'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    alpha: 'UnitInterval'
    red: 'UnitInterval'
    green: 'UnitInterval'
    blue: 'UnitInterval'
    swatchID: Optional['Uuid'] = None
UnitInterval = float

@dataclass_json
@dataclass
class GradientAsset(JSONMixin):
    class_: Literal['MSImmutableGradientAsset'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    do_objectID: 'Uuid'
    name: str
    gradient: 'Gradient'

@dataclass_json
@dataclass
class Gradient(JSONMixin):
    class_: Literal['gradient'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    gradientType: 'GradientType'
    elipseLength: float
    from_: 'PointString' = field(metadata={'fastclasses_json': {'field_name': 'from'}})
    to: 'PointString'
    stops: List['GradientStop']

class GradientType(Enum):
    Linear = 0
    Radial = 1
    Angular = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return GradientType.Undefined
PointString = str

@dataclass_json
@dataclass
class GradientStop(JSONMixin):
    class_: Literal['gradientStop'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    color: 'Color'
    position: 'UnitInterval'

@dataclass_json
@dataclass
class FileRef(JSONMixin):
    class_: Literal['MSJSONFileReference'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    ref_class: Union[Literal['MSImageData'], Literal['MSImmutablePage'], Literal['MSPatch']] = field(metadata={'fastclasses_json': {'field_name': '_ref_class'}})
    ref: str = field(metadata={'fastclasses_json': {'field_name': '_ref'}})

@dataclass_json
@dataclass
class DataRefData(JSONMixin):
    data: str = field(metadata={'fastclasses_json': {'field_name': '_data'}})

@dataclass_json
@dataclass
class DataRefSha1(JSONMixin):
    data: str = field(metadata={'fastclasses_json': {'field_name': '_data'}})

@dataclass_json
@dataclass
class DataRef(JSONMixin):
    class_: Literal['MSJSONOriginalDataReference'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    ref_class: Union[Literal['MSImageData'], Literal['MSFontData']] = field(metadata={'fastclasses_json': {'field_name': '_ref_class'}})
    ref: str = field(metadata={'fastclasses_json': {'field_name': '_ref'}})
    data: 'DataRefData'
    sha1: 'DataRefSha1'

class ColorSpace(Enum):
    Unmanaged = 0
    SRGB = 1
    P3 = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return ColorSpace.Undefined

@dataclass_json
@dataclass
class ForeignLayerStyle(JSONMixin):
    class_: Literal['MSImmutableForeignLayerStyle'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    do_objectID: 'Uuid'
    libraryID: 'Uuid'
    sourceLibraryName: str
    symbolPrivate: bool
    remoteStyleID: 'Uuid'
    localSharedStyle: 'SharedStyle'

@dataclass_json
@dataclass
class SharedStyle(JSONMixin):
    class_: Literal['sharedStyle'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    do_objectID: 'Uuid'
    name: str
    value: 'Style'

@dataclass_json
@dataclass
class Style(JSONMixin):
    class_: Literal['style'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    do_objectID: 'Uuid'
    borderOptions: 'BorderOptions'
    startMarkerType: 'MarkerType'
    endMarkerType: 'MarkerType'
    miterLimit: int
    windingRule: 'WindingRule'
    innerShadows: List['InnerShadow']
    colorControls: 'ColorControls'
    borders: Optional[List['Border']] = None
    blur: Optional['Blur'] = None
    fills: Optional[List['Fill']] = None
    textStyle: Optional['TextStyle'] = None
    shadows: Optional[List['Shadow']] = None
    contextSettings: Optional['GraphicsContextSettings'] = None

@dataclass_json
@dataclass
class Border(JSONMixin):
    class_: Literal['border'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    isEnabled: bool
    color: 'Color'
    fillType: 'FillType'
    position: 'BorderPosition'
    thickness: float
    contextSettings: 'GraphicsContextSettings'
    gradient: 'Gradient'

class FillType(Enum):
    Color = 0
    Gradient = 1
    Pattern = 4
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return FillType.Undefined

class BorderPosition(Enum):
    Center = 0
    Inside = 1
    Outside = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return BorderPosition.Undefined

@dataclass_json
@dataclass
class GraphicsContextSettings(JSONMixin):
    class_: Literal['graphicsContextSettings'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    blendMode: 'BlendMode'
    opacity: float

class BlendMode(Enum):
    Normal = 0
    Darken = 1
    Multiply = 2
    ColorBurn = 3
    Lighten = 4
    Screen = 5
    ColorDodge = 6
    Overlay = 7
    SoftLight = 8
    HardLight = 9
    Difference = 10
    Exclusion = 11
    Hue = 12
    Saturation = 13
    Color = 14
    Luminosity = 15
    PlusDarker = 16
    PlusLighter = 17
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return BlendMode.Undefined

@dataclass_json
@dataclass
class BorderOptions(JSONMixin):
    class_: Literal['borderOptions'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    isEnabled: bool
    dashPattern: List[float]
    lineCapStyle: 'LineCapStyle'
    lineJoinStyle: 'LineJoinStyle'

class LineCapStyle(Enum):
    Butt = 0
    Round = 1
    Projecting = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return LineCapStyle.Undefined

class LineJoinStyle(Enum):
    Miter = 0
    Round = 1
    Bevel = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return LineJoinStyle.Undefined

@dataclass_json
@dataclass
class Blur(JSONMixin):
    class_: Literal['blur'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    isEnabled: bool
    center: 'PointString'
    saturation: float
    type: 'BlurType'
    motionAngle: Optional[float] = None
    radius: Optional[float] = None

class BlurType(Enum):
    Gaussian = 0
    Motion = 1
    Zoom = 2
    Background = 3
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return BlurType.Undefined

@dataclass_json
@dataclass
class Fill(JSONMixin):
    class_: Literal['fill'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    isEnabled: bool
    color: 'Color'
    fillType: 'FillType'
    noiseIndex: float
    noiseIntensity: float
    patternFillType: 'PatternFillType'
    patternTileScale: float
    contextSettings: 'GraphicsContextSettings'
    gradient: 'Gradient'
    image: Optional[Union['FileRef', 'DataRef']] = None

class PatternFillType(Enum):
    Tile = 0
    Fill = 1
    Stretch = 2
    Fit = 3
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return PatternFillType.Undefined

class MarkerType(Enum):
    OpenArrow = 0
    FilledArrow = 1
    Line = 2
    OpenCircle = 3
    FilledCircle = 4
    OpenSquare = 5
    FilledSquare = 6
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return MarkerType.Undefined

class WindingRule(Enum):
    NonZero = 0
    EvenOdd = 1
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return WindingRule.Undefined

@dataclass_json
@dataclass
class TextStyleEncodedAttributes(JSONMixin):
    MSAttributedStringFontAttribute: 'FontDescriptor'
    paragraphStyle: Optional['ParagraphStyle'] = None
    MSAttributedStringTextTransformAttribute: Optional['TextTransform'] = None
    underlineStyle: Optional['UnderlineStyle'] = None
    strikethroughStyle: Optional['StrikethroughStyle'] = None
    kerning: Optional[float] = None
    textStyleVerticalAlignmentKey: Optional['TextVerticalAlignment'] = None
    MSAttributedStringColorAttribute: Optional['Color'] = None

@dataclass_json
@dataclass
class TextStyle(JSONMixin):
    class_: Literal['textStyle'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    verticalAlignment: 'TextVerticalAlignment'
    encodedAttributes: 'TextStyleEncodedAttributes'

class TextVerticalAlignment(Enum):
    Top = 0
    Middle = 1
    Bottom = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return TextVerticalAlignment.Undefined

@dataclass_json
@dataclass
class ParagraphStyle(JSONMixin):
    class_: Literal['paragraphStyle'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    alignment: Optional['TextHorizontalAlignment'] = None
    maximumLineHeight: Optional[float] = None
    minimumLineHeight: Optional[float] = None
    paragraphSpacing: Optional[float] = None
    allowsDefaultTighteningForTruncation: Optional[float] = None

class TextHorizontalAlignment(Enum):
    Left = 0
    Right = 1
    Centered = 2
    Justified = 3
    Natural = 4
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return TextHorizontalAlignment.Undefined

class TextTransform(Enum):
    None_ = 0
    Uppercase = 1
    Lowercase = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return TextTransform.Undefined

class UnderlineStyle(Enum):
    None_ = 0
    Underlined = 1
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return UnderlineStyle.Undefined

class StrikethroughStyle(Enum):
    None_ = 0
    Strikethrough = 1
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return StrikethroughStyle.Undefined

@dataclass_json
@dataclass
class FontDescriptorAttributes(JSONMixin):
    name: str
    size: float
    variation: Optional[Dict[str, float]] = None

@dataclass_json
@dataclass
class FontDescriptor(JSONMixin):
    class_: Literal['fontDescriptor'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    attributes: 'FontDescriptorAttributes'

@dataclass_json
@dataclass
class Shadow(JSONMixin):
    class_: Literal['shadow'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    isEnabled: bool
    blurRadius: float
    color: 'Color'
    contextSettings: 'GraphicsContextSettings'
    offsetX: float
    offsetY: float
    spread: float

@dataclass_json
@dataclass
class InnerShadow(JSONMixin):
    class_: Literal['innerShadow'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    isEnabled: bool
    blurRadius: float
    color: 'Color'
    contextSettings: 'GraphicsContextSettings'
    offsetX: float
    offsetY: float
    spread: float

@dataclass_json
@dataclass
class ColorControls(JSONMixin):
    class_: Literal['colorControls'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    isEnabled: bool
    brightness: float
    contrast: float
    hue: float
    saturation: float

@dataclass_json
@dataclass
class ForeignSymbol(JSONMixin):
    class_: Literal['MSImmutableForeignSymbol'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    do_objectID: 'Uuid'
    libraryID: 'Uuid'
    sourceLibraryName: str
    symbolPrivate: bool
    originalMaster: 'SymbolMaster'
    symbolMaster: 'SymbolMaster'
    missingLibraryFontAcknowledged: Optional[bool] = None

@dataclass_json
@dataclass
class SymbolMaster(JSONMixin):
    class_: Literal['symbolMaster'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    allowsOverrides: bool
    backgroundColor: 'Color'
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    hasBackgroundColor: bool
    hasClickThrough: bool
    horizontalRulerData: 'RulerData'
    includeBackgroundColorInExport: bool
    includeBackgroundColorInInstance: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isFlowHome: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    layers: List[Union['Group', 'Oval', 'Polygon', 'Rectangle', 'ShapePath', 'Star', 'Triangle', 'ShapeGroup', 'Text', 'SymbolInstance', 'Slice', 'Hotspot', 'Bitmap']] = field(metadata={'fastclasses_json': {'decoder': lambda lst: [to_object(x) for x in lst if x is not None]}})
    name: str
    nameIsFixed: bool
    overrideProperties: List['OverrideProperty']
    resizesContent: bool
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    symbolID: 'Uuid'
    verticalRulerData: 'RulerData'
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None
    layout: Optional['LayoutGrid'] = None
    grid: Optional['SimpleGrid'] = None
    groupLayout: Optional[Union['FreeformGroupLayout', 'InferredGroupLayout']] = None
    presetDictionary: Optional[Any] = None

class BooleanOperation(Enum):
    None_ = -1
    Union = 0
    Subtract = 1
    Intersection = 2
    Difference = 3
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return BooleanOperation.Undefined

@dataclass_json
@dataclass
class ExportOptions(JSONMixin):
    class_: Literal['exportOptions'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    exportFormats: List['ExportFormat']
    includedLayerIds: List['Uuid']
    layerOptions: int
    shouldTrim: bool

@dataclass_json
@dataclass
class ExportFormat(JSONMixin):
    class_: Literal['exportFormat'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    absoluteSize: int
    fileFormat: 'ExportFileFormat'
    name: str
    scale: float
    visibleScaleType: 'VisibleScaleType'
    namingScheme: Optional['ExportFormatNamingScheme'] = None

class ExportFileFormat(Enum):
    PNG = 'png'
    JPG = 'jpg'
    TIFF = 'tiff'
    EPS = 'eps'
    PDF = 'pdf'
    WEBP = 'webp'
    SVG = 'svg'
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return ExportFileFormat.Undefined

class ExportFormatNamingScheme(Enum):
    Suffix = 0
    SecondaryPrefix = 1
    PrimaryPrefix = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return ExportFormatNamingScheme.Undefined

class VisibleScaleType(Enum):
    Scale = 0
    Width = 1
    Height = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return VisibleScaleType.Undefined

@dataclass_json
@dataclass
class Rect(JSONMixin):
    class_: Literal['rect'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    constrainProportions: bool
    height: float
    width: float
    x: float
    y: float

@dataclass_json
@dataclass
class FlowConnection(JSONMixin):
    class_: Literal['MSImmutableFlowConnection'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    destinationArtboardID: Union['Uuid', Literal['back']]
    animationType: 'AnimationType'
    maintainScrollPosition: Optional[bool] = None

class AnimationType(Enum):
    None_ = 0
    SlideFromLeft = 1
    SlideFromRight = 2
    SlideFromBottom = 3
    SlideFromTop = 4
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return AnimationType.Undefined

class LayerListExpanded(Enum):
    Undecided = 0
    Collapsed = 1
    Expanded = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return LayerListExpanded.Undefined

class ResizeType(Enum):
    Stretch = 0
    PinToEdge = 1
    Resize = 2
    Float = 3
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return ResizeType.Undefined

@dataclass_json
@dataclass
class RulerData(JSONMixin):
    class_: Literal['rulerData'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    base: int
    guides: List[int]

@dataclass_json
@dataclass
class LayoutGrid(JSONMixin):
    class_: Literal['layoutGrid'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    isEnabled: bool
    columnWidth: int
    gutterHeight: int
    gutterWidth: int
    horizontalOffset: int
    numberOfColumns: int
    rowHeightMultiplication: int
    totalWidth: int
    guttersOutside: bool
    drawHorizontal: bool
    drawHorizontalLines: bool
    drawVertical: bool

@dataclass_json
@dataclass
class SimpleGrid(JSONMixin):
    class_: Literal['simpleGrid'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    isEnabled: bool
    gridSize: int
    thickGridTimes: int

@dataclass_json
@dataclass
class FreeformGroupLayout(JSONMixin):
    class_: Literal['MSImmutableFreeformGroupLayout'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})

@dataclass_json
@dataclass
class InferredGroupLayout(JSONMixin):
    class_: Literal['MSImmutableInferredGroupLayout'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    axis: 'InferredLayoutAxis'
    layoutAnchor: 'InferredLayoutAnchor'
    maxSize: Optional[float] = None
    minSize: Optional[float] = None

class InferredLayoutAxis(Enum):
    Horizontal = 0
    Vertical = 1
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return InferredLayoutAxis.Undefined

class InferredLayoutAnchor(Enum):
    Min = 0
    Middle = 1
    Max = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return InferredLayoutAnchor.Undefined

@dataclass_json
@dataclass
class OverrideProperty(JSONMixin):
    class_: Literal['MSImmutableOverrideProperty'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    overrideName: 'OverrideName'
    canOverride: bool
OverrideName = Union[str, str, str, str]

@dataclass_json
@dataclass
class Group(JSONMixin):
    class_: Literal['group'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    hasClickThrough: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    layers: List[Union['Group', 'Oval', 'Polygon', 'Rectangle', 'ShapePath', 'Star', 'Triangle', 'ShapeGroup', 'Text', 'SymbolInstance', 'Slice', 'Hotspot', 'Bitmap']] = field(metadata={'fastclasses_json': {'decoder': lambda lst: [to_object(x) for x in lst if x is not None]}})
    name: str
    nameIsFixed: bool
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None
    groupLayout: Optional[Union['FreeformGroupLayout', 'InferredGroupLayout']] = None

@dataclass_json
@dataclass
class Oval(JSONMixin):
    class_: Literal['oval'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    edited: bool
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    isClosed: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    name: str
    nameIsFixed: bool
    pointRadiusBehaviour: 'PointsRadiusBehaviour'
    points: List['CurvePoint']
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

class PointsRadiusBehaviour(Enum):
    Disabled = -1
    Legacy = 0
    Rounded = 1
    Smooth = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return PointsRadiusBehaviour.Undefined

@dataclass_json
@dataclass
class CurvePoint(JSONMixin):
    class_: Literal['curvePoint'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    cornerRadius: float
    cornerStyle: 'CornerStyle'
    curveFrom: 'PointString'
    curveTo: 'PointString'
    hasCurveFrom: bool
    hasCurveTo: bool
    curveMode: 'CurveMode'
    point: 'PointString'

class CornerStyle(Enum):
    Rounded = 0
    RoundedInverted = 1
    Angled = 2
    Squared = 3
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return CornerStyle.Undefined

class CurveMode(Enum):
    None_ = 0
    Straight = 1
    Mirrored = 2
    Asymmetric = 3
    Disconnected = 4
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return CurveMode.Undefined

@dataclass_json
@dataclass
class Polygon(JSONMixin):
    class_: Literal['polygon'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    edited: bool
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    isClosed: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    name: str
    nameIsFixed: bool
    numberOfPoints: int
    pointRadiusBehaviour: 'PointsRadiusBehaviour'
    points: List['CurvePoint']
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

@dataclass_json
@dataclass
class Rectangle(JSONMixin):
    class_: Literal['rectangle'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    edited: bool
    exportOptions: 'ExportOptions'
    fixedRadius: float
    frame: 'Rect'
    hasConvertedToNewRoundCorners: bool
    isClosed: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    name: str
    nameIsFixed: bool
    needsConvertionToNewRoundCorners: bool
    pointRadiusBehaviour: 'PointsRadiusBehaviour'
    points: List['CurvePoint']
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

@dataclass_json
@dataclass
class ShapePath(JSONMixin):
    class_: Literal['shapePath'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    edited: bool
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    isClosed: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    name: str
    nameIsFixed: bool
    pointRadiusBehaviour: 'PointsRadiusBehaviour'
    points: List['CurvePoint']
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

@dataclass_json
@dataclass
class Star(JSONMixin):
    class_: Literal['star'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    edited: bool
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    isClosed: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    name: str
    nameIsFixed: bool
    numberOfPoints: int
    pointRadiusBehaviour: 'PointsRadiusBehaviour'
    points: List['CurvePoint']
    radius: float
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

@dataclass_json
@dataclass
class Triangle(JSONMixin):
    class_: Literal['triangle'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    edited: bool
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    isClosed: bool
    isEquilateral: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    name: str
    nameIsFixed: bool
    pointRadiusBehaviour: 'PointsRadiusBehaviour'
    points: List['CurvePoint']
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

@dataclass_json
@dataclass
class ShapeGroup(JSONMixin):
    class_: Literal['shapeGroup'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    hasClickThrough: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    layers: List[Union['Group', 'Oval', 'Polygon', 'Rectangle', 'ShapePath', 'Star', 'Triangle', 'ShapeGroup', 'Text', 'SymbolInstance', 'Slice', 'Hotspot', 'Bitmap']] = field(metadata={'fastclasses_json': {'decoder': lambda lst: [to_object(x) for x in lst if x is not None]}})
    name: str
    nameIsFixed: bool
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    windingRule: 'WindingRule'
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None
    groupLayout: Optional[Union['FreeformGroupLayout', 'InferredGroupLayout']] = None

@dataclass_json
@dataclass
class Text(JSONMixin):
    class_: Literal['text'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    attributedString: 'AttributedString'
    automaticallyDrawOnUnderlyingPath: bool
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    dontSynchroniseWithSymbol: bool
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    glyphBounds: 'PointListString'
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    lineSpacingBehaviour: 'LineSpacingBehaviour'
    name: str
    nameIsFixed: bool
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    textBehaviour: 'TextBehaviour'
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

@dataclass_json
@dataclass
class AttributedString(JSONMixin):
    class_: Literal['attributedString'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    string: str
    attributes: List['StringAttribute']

@dataclass_json
@dataclass
class StringAttributeAttributes(JSONMixin):
    MSAttributedStringFontAttribute: 'FontDescriptor'
    kerning: Optional[float] = None
    textStyleVerticalAlignmentKey: Optional['TextVerticalAlignment'] = None
    MSAttributedStringColorAttribute: Optional['Color'] = None
    paragraphStyle: Optional['ParagraphStyle'] = None

@dataclass_json
@dataclass
class StringAttribute(JSONMixin):
    class_: Literal['stringAttribute'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    location: int
    length: int
    attributes: 'StringAttributeAttributes'

class LineSpacingBehaviour(Enum):
    None_ = 0
    Legacy = 1
    ConsistentBaseline = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return LineSpacingBehaviour.Undefined

class TextBehaviour(Enum):
    Flexible = 0
    Fixed = 1
    FixedWidthAndHeight = 2
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return TextBehaviour.Undefined
PointListString = str

@dataclass_json
@dataclass
class SymbolInstance(JSONMixin):
    class_: Literal['symbolInstance'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    horizontalSpacing: float
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    name: str
    nameIsFixed: bool
    overrideValues: List['OverrideValue']
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    scale: float
    shouldBreakMaskChain: bool
    symbolID: 'Uuid'
    verticalSpacing: float
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

@dataclass_json
@dataclass
class OverrideValue(JSONMixin):
    class_: Literal['overrideValue'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    overrideName: 'OverrideName'
    value: Union[str, 'Uuid', 'FileRef', 'DataRef']
    do_objectID: Optional['Uuid'] = None

@dataclass_json
@dataclass
class Slice(JSONMixin):
    class_: Literal['slice'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    backgroundColor: 'Color'
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    hasBackgroundColor: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    name: str
    nameIsFixed: bool
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

@dataclass_json
@dataclass
class Hotspot(JSONMixin):
    class_: Literal['MSImmutableHotspotLayer'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    name: str
    nameIsFixed: bool
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

@dataclass_json
@dataclass
class Bitmap(JSONMixin):
    class_: Literal['bitmap'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    clippingMask: 'PointListString'
    do_objectID: 'Uuid'
    exportOptions: 'ExportOptions'
    fillReplacesImage: bool
    frame: 'Rect'
    image: Union['FileRef', 'DataRef']
    intendedDPI: int
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    name: str
    nameIsFixed: bool
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None

@dataclass_json
@dataclass
class ForeignTextStyle(JSONMixin):
    class_: Literal['MSImmutableForeignTextStyle'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    libraryID: 'Uuid'
    sourceLibraryName: str
    symbolPrivate: bool
    remoteStyleID: 'Uuid'
    localSharedStyle: 'SharedStyle'
    missingLibraryFontAcknowledged: Optional[bool] = None

@dataclass_json
@dataclass
class ForeignSwatch(JSONMixin):
    class_: Literal['MSImmutableForeignSwatch'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    do_objectID: 'Uuid'
    libraryID: 'Uuid'
    sourceLibraryName: str
    symbolPrivate: bool
    remoteSwatchID: 'Uuid'
    localSwatch: 'Swatch'

@dataclass_json
@dataclass
class Swatch(JSONMixin):
    class_: Literal['swatch'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    do_objectID: 'Uuid'
    name: str
    value: 'Color'

@dataclass_json
@dataclass
class SharedStyleContainer(JSONMixin):
    class_: Literal['sharedStyleContainer'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    objects: List['SharedStyle']
    do_objectID: Optional['Uuid'] = None

@dataclass_json
@dataclass
class SharedTextStyleContainer(JSONMixin):
    class_: Literal['sharedTextStyleContainer'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    objects: List['SharedStyle']
    do_objectID: Optional['Uuid'] = None

@dataclass_json
@dataclass
class SymbolContainer(JSONMixin):
    class_: Literal['symbolContainer'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    objects: List[Any]
    do_objectID: Optional['Uuid'] = None

@dataclass_json
@dataclass
class SwatchContainer(JSONMixin):
    class_: Literal['swatchContainer'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    objects: List['Swatch']
    do_objectID: Optional['Uuid'] = None

@dataclass_json
@dataclass
class FontRef(JSONMixin):
    class_: Literal['fontReference'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    fontData: 'DataRef'
    fontFamilyName: str
    fontFileName: str
    options: int
    postscriptNames: List[str]
DocumentState = Any

@dataclass_json
@dataclass
class PatchInfo(JSONMixin):
    class_: Literal['MSImmutablePatchInfo'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    baseVersionID: 'Uuid'
    lastIntegratedPatchID: 'Uuid'
    localPatches: List['FileRef']
    receivedPatches: List['FileRef']

@dataclass_json
@dataclass
class Page(JSONMixin):
    class_: Literal['page'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    hasClickThrough: bool
    horizontalRulerData: 'RulerData'
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    layers: List[Union['Artboard', 'Group', 'Oval', 'Polygon', 'Rectangle', 'ShapePath', 'Star', 'Triangle', 'ShapeGroup', 'Text', 'SymbolMaster', 'SymbolInstance', 'Slice', 'Hotspot', 'Bitmap']] = field(metadata={'fastclasses_json': {'decoder': lambda lst: [to_object(x) for x in lst if x is not None]}})
    name: str
    nameIsFixed: bool
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    verticalRulerData: 'RulerData'
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None
    layout: Optional['LayoutGrid'] = None
    grid: Optional['SimpleGrid'] = None
    groupLayout: Optional[Union['FreeformGroupLayout', 'InferredGroupLayout']] = None

@dataclass_json
@dataclass
class Artboard(JSONMixin):
    class_: Literal['artboard'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    backgroundColor: 'Color'
    booleanOperation: 'BooleanOperation'
    do_objectID: 'Uuid'
    exportOptions: 'ExportOptions'
    frame: 'Rect'
    hasBackgroundColor: bool
    hasClickThrough: bool
    horizontalRulerData: 'RulerData'
    includeBackgroundColorInExport: bool
    isFixedToViewport: bool
    isFlippedHorizontal: bool
    isFlippedVertical: bool
    isFlowHome: bool
    isLocked: bool
    isVisible: bool
    layerListExpandedType: 'LayerListExpanded'
    layers: List[Union['Group', 'Oval', 'Polygon', 'Rectangle', 'ShapePath', 'Star', 'Triangle', 'ShapeGroup', 'Text', 'SymbolInstance', 'Slice', 'Hotspot', 'Bitmap']] = field(metadata={'fastclasses_json': {'decoder': lambda lst: [to_object(x) for x in lst if x is not None]}})
    name: str
    nameIsFixed: bool
    resizesContent: bool
    resizingConstraint: int
    resizingType: 'ResizeType'
    rotation: float
    shouldBreakMaskChain: bool
    verticalRulerData: 'RulerData'
    flow: Optional['FlowConnection'] = None
    sharedStyleID: Optional['Uuid'] = None
    hasClippingMask: Optional[bool] = None
    clippingMaskMode: Optional[int] = None
    userInfo: Optional[Any] = None
    style: Optional['Style'] = None
    maintainScrollPosition: Optional[bool] = None
    layout: Optional['LayoutGrid'] = None
    grid: Optional['SimpleGrid'] = None
    groupLayout: Optional[Union['FreeformGroupLayout', 'InferredGroupLayout']] = None
    presetDictionary: Optional[Any] = None

@dataclass_json
@dataclass
class MetaPagesAndArtboardsValueArtboardsValue(JSONMixin):
    name: str

@dataclass_json
@dataclass
class MetaPagesAndArtboardsValue(JSONMixin):
    name: str
    artboards: Dict[str, 'MetaPagesAndArtboardsValueArtboardsValue']

@dataclass_json
@dataclass
class MetaCreated(JSONMixin):
    commit: str
    appVersion: str
    build: int
    app: 'BundleId'
    compatibilityVersion: float
    version: float
    variant: 'SketchVariant'
    coeditCompatibilityVersion: Optional[float] = None

@dataclass_json
@dataclass
class Meta(JSONMixin):
    commit: str
    pagesAndArtboards: Dict[str, 'MetaPagesAndArtboardsValue']
    version: Union[Literal[121], Literal[122], Literal[123], Literal[124], Literal[125], Literal[126], Literal[127], Literal[128], Literal[129], Literal[130], Literal[131], Literal[132], Literal[133], Literal[134], Literal[135], Literal[136], Literal[137], Literal[138], Literal[139]]
    compatibilityVersion: Literal[99]
    app: 'BundleId'
    autosaved: 'NumericalBool'
    variant: 'SketchVariant'
    created: 'MetaCreated'
    saveHistory: List[str]
    appVersion: str
    build: int
    coeditCompatibilityVersion: Optional[float] = None

class BundleId(Enum):
    PublicRelease = 'com.bohemiancoding.sketch3'
    Beta = 'com.bohemiancoding.sketch3.beta'
    Private = 'com.bohemiancoding.sketch3.private'
    FeaturePreview = 'com.bohemiancoding.sketch3.feature-preview'
    Internal = 'com.bohemiancoding.sketch3.internal'
    Experimental = 'com.bohemiancoding.sketch3.experimental'
    Testing = 'com.bohemiancoding.sketch3.testing'
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return BundleId.Undefined

class NumericalBool(Enum):
    True_ = 0
    False_ = 1
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return NumericalBool.Undefined
SketchVariant = Union[Literal['NONAPPSTORE'], Literal['APPSTORE'], Literal['BETA'], Literal['PRIVATE'], Literal['FEATURE_PREVIEW'], Literal['INTERNAL'], Literal['EXPERIMENTAL'], Literal['TESTING'], Literal['UNITTEST']]
User = Dict[str, Any]
Workspace = Any

@dataclass_json
@dataclass
class ContentsDocument(JSONMixin):
    class_: Literal['document'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    assets: 'AssetCollection'
    colorSpace: 'ColorSpace'
    currentPageIndex: int
    do_objectID: 'Uuid'
    foreignLayerStyles: List['ForeignLayerStyle']
    foreignSymbols: List['ForeignSymbol']
    foreignTextStyles: List['ForeignTextStyle']
    layerStyles: 'SharedStyleContainer'
    layerTextStyles: 'SharedTextStyleContainer'
    pages: List['Page']
    foreignSwatches: Optional[List['ForeignSwatch']] = None
    layerSymbols: Optional['SymbolContainer'] = None
    sharedSwatches: Optional['SwatchContainer'] = None
    fontReferences: Optional[List['FontRef']] = None
    documentState: Optional['DocumentState'] = None
    patchInfo: Optional['PatchInfo'] = None

@dataclass_json
@dataclass
class Contents(JSONMixin):
    document: 'ContentsDocument'
    meta: 'Meta'
    user: 'User'
    workspace: Optional['Workspace'] = None

@dataclass_json
@dataclass
class Document(JSONMixin):
    class_: Literal['document'] = field(metadata={'fastclasses_json': {'field_name': '_class'}})
    assets: 'AssetCollection'
    colorSpace: 'ColorSpace'
    currentPageIndex: int
    do_objectID: 'Uuid'
    foreignLayerStyles: List['ForeignLayerStyle']
    foreignSymbols: List['ForeignSymbol']
    foreignTextStyles: List['ForeignTextStyle']
    layerStyles: 'SharedStyleContainer'
    layerTextStyles: 'SharedTextStyleContainer'
    pages: List['FileRef']
    foreignSwatches: Optional[List['ForeignSwatch']] = None
    layerSymbols: Optional['SymbolContainer'] = None
    sharedSwatches: Optional['SwatchContainer'] = None
    fontReferences: Optional[List['FontRef']] = None
    documentState: Optional['DocumentState'] = None
    patchInfo: Optional['PatchInfo'] = None
AnyLayer = Union['SymbolMaster', 'Group', 'Oval', 'Polygon', 'Rectangle', 'ShapePath', 'Star', 'Triangle', 'ShapeGroup', 'Text', 'SymbolInstance', 'Slice', 'Hotspot', 'Bitmap', 'Page', 'Artboard']
AnyGroup = Union['SymbolMaster', 'Group', 'ShapeGroup', 'Page', 'Artboard']
AnyObject = Union['AssetCollection', 'ImageCollection', 'ColorAsset', 'Color', 'GradientAsset', 'Gradient', 'GradientStop', 'FileRef', 'DataRef', 'ForeignLayerStyle', 'SharedStyle', 'Style', 'Border', 'GraphicsContextSettings', 'BorderOptions', 'Blur', 'Fill', 'TextStyle', 'ParagraphStyle', 'FontDescriptor', 'Shadow', 'InnerShadow', 'ColorControls', 'ForeignSymbol', 'SymbolMaster', 'ExportOptions', 'ExportFormat', 'Rect', 'FlowConnection', 'RulerData', 'LayoutGrid', 'SimpleGrid', 'FreeformGroupLayout', 'InferredGroupLayout', 'OverrideProperty', 'Group', 'Oval', 'CurvePoint', 'Polygon', 'Rectangle', 'ShapePath', 'Star', 'Triangle', 'ShapeGroup', 'Text', 'AttributedString', 'StringAttribute', 'SymbolInstance', 'OverrideValue', 'Slice', 'Hotspot', 'Bitmap', 'ForeignTextStyle', 'ForeignSwatch', 'Swatch', 'SharedStyleContainer', 'SharedTextStyleContainer', 'SymbolContainer', 'SwatchContainer', 'FontRef', 'PatchInfo', 'Page', 'Artboard']

class ClassValue(Enum):
    SharedTextStyleContainer = 'sharedTextStyleContainer'
    MSImmutableInferredGroupLayout = 'MSImmutableInferredGroupLayout'
    ShapePath = 'shapePath'
    MSImmutableForeignSymbol = 'MSImmutableForeignSymbol'
    GradientStop = 'gradientStop'
    OverrideValue = 'overrideValue'
    Group = 'group'
    Artboard = 'artboard'
    Border = 'border'
    MSImmutableGradientAsset = 'MSImmutableGradientAsset'
    Star = 'star'
    RulerData = 'rulerData'
    CurvePoint = 'curvePoint'
    MSImmutableColorAsset = 'MSImmutableColorAsset'
    TextStyle = 'textStyle'
    GraphicsContextSettings = 'graphicsContextSettings'
    ExportFormat = 'exportFormat'
    MSJSONFileReference = 'MSJSONFileReference'
    Bitmap = 'bitmap'
    SharedStyleContainer = 'sharedStyleContainer'
    LayoutGrid = 'layoutGrid'
    Style = 'style'
    BorderOptions = 'borderOptions'
    Color = 'color'
    Oval = 'oval'
    SwatchContainer = 'swatchContainer'
    SymbolInstance = 'symbolInstance'
    InnerShadow = 'innerShadow'
    Rect = 'rect'
    Page = 'page'
    MSImmutableFreeformGroupLayout = 'MSImmutableFreeformGroupLayout'
    SharedStyle = 'sharedStyle'
    Blur = 'blur'
    ParagraphStyle = 'paragraphStyle'
    FontReference = 'fontReference'
    SimpleGrid = 'simpleGrid'
    MSImmutableForeignLayerStyle = 'MSImmutableForeignLayerStyle'
    Fill = 'fill'
    MSImmutableFlowConnection = 'MSImmutableFlowConnection'
    MSJSONOriginalDataReference = 'MSJSONOriginalDataReference'
    FontDescriptor = 'fontDescriptor'
    Slice = 'slice'
    Gradient = 'gradient'
    Polygon = 'polygon'
    MSImmutableForeignTextStyle = 'MSImmutableForeignTextStyle'
    StringAttribute = 'stringAttribute'
    Triangle = 'triangle'
    MSImmutableForeignSwatch = 'MSImmutableForeignSwatch'
    ExportOptions = 'exportOptions'
    MSImmutablePatchInfo = 'MSImmutablePatchInfo'
    AttributedString = 'attributedString'
    Swatch = 'swatch'
    ShapeGroup = 'shapeGroup'
    SymbolContainer = 'symbolContainer'
    Shadow = 'shadow'
    Text = 'text'
    Rectangle = 'rectangle'
    ColorControls = 'colorControls'
    SymbolMaster = 'symbolMaster'
    MSImmutableHotspotLayer = 'MSImmutableHotspotLayer'
    MSImmutableOverrideProperty = 'MSImmutableOverrideProperty'
    AssetCollection = 'assetCollection'
    ImageCollection = 'imageCollection'
    Undefined = object()

    @classmethod
    def _missing_(cls, value):
        return ClassValue.Undefined
class_map: Dict[str, Type[JSONMixin]] = {'sharedTextStyleContainer': SharedTextStyleContainer, 'MSImmutableInferredGroupLayout': InferredGroupLayout, 'shapePath': ShapePath, 'MSImmutableForeignSymbol': ForeignSymbol, 'gradientStop': GradientStop, 'overrideValue': OverrideValue, 'group': Group, 'artboard': Artboard, 'border': Border, 'MSImmutableGradientAsset': GradientAsset, 'star': Star, 'rulerData': RulerData, 'curvePoint': CurvePoint, 'MSImmutableColorAsset': ColorAsset, 'textStyle': TextStyle, 'graphicsContextSettings': GraphicsContextSettings, 'exportFormat': ExportFormat, 'MSJSONFileReference': FileRef, 'bitmap': Bitmap, 'sharedStyleContainer': SharedStyleContainer, 'layoutGrid': LayoutGrid, 'style': Style, 'borderOptions': BorderOptions, 'color': Color, 'oval': Oval, 'swatchContainer': SwatchContainer, 'symbolInstance': SymbolInstance, 'innerShadow': InnerShadow, 'rect': Rect, 'page': Page, 'MSImmutableFreeformGroupLayout': FreeformGroupLayout, 'sharedStyle': SharedStyle, 'blur': Blur, 'paragraphStyle': ParagraphStyle, 'fontReference': FontRef, 'simpleGrid': SimpleGrid, 'MSImmutableForeignLayerStyle': ForeignLayerStyle, 'fill': Fill, 'MSImmutableFlowConnection': FlowConnection, 'MSJSONOriginalDataReference': DataRef, 'fontDescriptor': FontDescriptor, 'slice': Slice, 'gradient': Gradient, 'polygon': Polygon, 'MSImmutableForeignTextStyle': ForeignTextStyle, 'stringAttribute': StringAttribute, 'triangle': Triangle, 'MSImmutableForeignSwatch': ForeignSwatch, 'exportOptions': ExportOptions, 'MSImmutablePatchInfo': PatchInfo, 'attributedString': AttributedString, 'swatch': Swatch, 'shapeGroup': ShapeGroup, 'symbolContainer': SymbolContainer, 'shadow': Shadow, 'text': Text, 'rectangle': Rectangle, 'colorControls': ColorControls, 'symbolMaster': SymbolMaster, 'MSImmutableHotspotLayer': Hotspot, 'MSImmutableOverrideProperty': OverrideProperty, 'assetCollection': AssetCollection, 'imageCollection': ImageCollection}