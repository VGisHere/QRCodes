# import modules
import qrcode
from PIL import Image
import vobject
from qrcode.image.styledpil import *
from qrcode.image.svg import *
from qrcode.image.pure import *
from qrcode.image.styles.moduledrawers import *
from qrcode.image.styles.colormasks import *
import argparse
 
# taking image which user wants
# in the QR code center
Logo_link = 'VG.png'
 
logo = Image.open(Logo_link)
 
# taking base width
basewidth = 355
 
# adjust image size
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
 
# generating QR code
QRcode.make(fit=True)
 
# taking color name from user
QRcolor = 'magenta'

# adding color to QR code
QRimg = QRcode.make_image( fill_color=QRcolor, back_color="white",
                           image_factory=StyledPilImage, 
                           module_drawer=RoundedModuleDrawer(),
                           #color_mask=RadialGradiantColorMask(edge_color = (255,0,255))
                           #color_mask=ImageColorMask(back_color=(255, 255, 255), color_mask_path=None, color_mask_image=None)
                           #color_mask=SolidFillColorMask(back_color=(255, 255, 255, False), front_color=(0, 0, 0))
                           #color_mask=SquareGradiantColorMask(center_color = (0,0,0), edge_color = (255,0,255))
                           #color_mask=HorizontalGradiantColorMask(back_color=(255, 255, 255), left_color=(255, 0, 255), right_color=(0, 255, 255))
                           color_mask=VerticalGradiantColorMask(top_color = (255,0,255), bottom_color = (0,255,255))
                         ).convert('RGB')
 
# set size of QR code
pos = ((QRimg.size[0] - logo.size[0]) // 2,
       (QRimg.size[1] - logo.size[1]) // 2)
QRimg.paste(logo, pos)

#qrcode.paste(logo, pos)

# save the QR code generated
QRimg.save('VGisHere_QR.png')


class vCardProperties():
    def __init__(self):
        self.fname = None
        self.name  = None
        self.weblist  = []
        self.maillist = []
        self.tellist  = []
        self.region   = ''
        self.country  = ''

def QRCodeProperties():
    def __init__(self):
        self.bgcolor = ''
        self.fgcolor = ''
        self.edcolor = ''
        self.ctcolor = ''
        self.stcolor = ''
        self.endcolor = ''
        
        self.logo_path      =   None
        self.logo_size      =   'medium'
        self.img_mask_path  =   None
        self.shape          =   ''
        self.color_mask     =   ''
        self.img_type       =   ''
        

def main(vCardProp: vCardProperties, QRProp: QRCodeProperties, outfile: str):
    
    if QRProp.logo_path:
        logo = Image.open(QRProp.logo_path)
 
        # taking base width
        basewidth = 355 if QRProp.logo_size.lower() == 'medium' else \
                    (255 if QRProp.logo_size.lower() == 'small' else 455)
 
        # adjust image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    vCrd = vobject.vCard()
    vCrd.add('fn').value = vCardProp.name
    vCrd.add('n').value = vobject.vcard.Name(family=vCardProp.name.split()[-1], given=vCardProp.name.split()[0])

    for url in vCardProp.weblist:
        vCrd.add('url').value = url
    
    for ml in vCardProp.maillist:
        vCrd.add('email').value = ml
    
    for tl in vCardProp.maillist:
        vCrd.add('email').value = tl
 
    # adding URL or text to QRcode
    QRcode.add_data(vCrd.serialize())
 
    # generating QR code
    QRcode.make(fit=True)

    img_fctry = {
                'StyledPNG' : StyledPilImage,
                'PurePNG'   : PymagingImage,
                'SVG'       : SvgImage
                 }
    
    clr_msk = {
                'SolidFill'            : SolidFillColorMask,
                'RadialGradiant'       : RadialGradiantColorMask,
                'SquareGradiant'       : SquareGradiantColorMask,
                'HorizontalGradiant'   : HorizontalGradiantColorMask,
                'VerticalGradiant'     : VerticalGradiantColorMask,
                'Image'                : ImageColorMask
            }
    
    mdl_drwr = {
                'Square'            : SquareModuleDrawer,
                'GappedSquare'      : GappedSquareModuleDrawer,
                'Circle'            : CircleModuleDrawer,
                'HorizontalBars'    : HorizontalBarsDrawer,
                'Rounded'           : RoundedModuleDrawer,
                'VerticalBars'      : VerticalBarsDrawer,
                }
    
    QRimg = QRcode.make_image(fill_color = QRProp.fgcolor, back_color=QRProp.bgcolor,
                           image_factory = img_fctry[QRProp.img_type], 
                           module_drawer = mdl_drwr[QRProp.shape](),
                           color_mask    = clr_msk[QRProp.color_mask](top_color = (255,0,255), bottom_color = (0,255,255))
                         ).convert('RGB')
    
    if QRProp.logo_path:
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)

        QRimg.paste(logo, pos)

    # save the QR code generated
    QRimg.save(outfile)

def parseFromVCF(vcf_file_path):
    pass

if __name__ == 'main':
    
    parser = argparse.ArgumentParser(description='')
    
    # Data Fields
    parser.add_argument('-fn',      '--formatted_name',     help='Display Name for vCard')
    parser.add_argument('-n',       '--name',               default='', help='Actual Name for vCard')
    parser.add_argument('-web',     '--website',            default='', help='Personal Website',    action='append', nargs='+')
    parser.add_argument('-email',   '--email',              default='', help='Email for vCard',     action='append', nargs='+')
    parser.add_argument('-tel',     '--telephone',          default='', help='Telephone No.',       action='append', nargs='+')
    parser.add_argument('-rg',      '--region',             default='', help='Region of residence')
    parser.add_argument('-cn',      '--country',            default='', help='Country of residence')
    
    # Or pick data from vcf (.txt) file
    parser.add_argument('-vf',      '--contact_file',       help='Use text file containing data in standard VCF format')
    
    # QR Customisation
    parser.add_argument('-bg',      '--back_color',         default='white',    help='Background Color')
    parser.add_argument('-fg',      '--fore_color',         default='black',    help='Foreground Color')
    parser.add_argument('-lgsz',    '--logo_size',          default='Medium',   help='Logo Size : Small, Medium, Large')
    parser.add_argument('-logo',    '--logo_path',          default=None,       help='Insert mentioned image as logo in QR code')
    parser.add_argument('-cmask',   '--color_mask',         default='SolidFill',       
                        choices = ['SolidFill', 'RadialGradiant', 'SquareGradiant',
                                   'HorizontalGradiant', 'VerticalGradiant', 'Image'],
                        help='Insert mentioned image as logo in QR code')
    
    parser.add_argument('-lshape',  '--line_shape',         default='Square',    
                        choices = ['Square',    'GappedSquare',
                                   'Circle',    'HorizontalBars',
                                   'Rounded',   'VerticalBars'],
                        
                        help='Choose shape for QR code data lines')
    
    parser.add_argument('-img',     '--image_type',         default='StyledPNG',    
                        choices = ['StyledPNG', 'SVG', 'PurePNG'],
                        help='End Color for Horizontal/Vertical Gradient')
    # PymagingImage : PNG without QR customisations
    # StyledPIL     : PNG with QR customisations
    
    parser.add_argument('-edgclr',  '--edge_color',         default='#000000',    help='Edge Color for Radial Gradient')
    parser.add_argument('-cntclr',  '--center_color',       default='#000000',    help='Center Color for Radial Gradient')
    parser.add_argument('-strtclr', '--start_color',        default='#000000',    help='Start Color for Horizontal/Vertical Gradient')
    parser.add_argument('-endclr',  '--end_color',          default='#000000',    help='End Color for Horizontal/Vertical Gradient')
    
    parser.add_argument('-imask',    '--image_mask_path',   default=None,       help='Use mentioned image as foreground color in QR code')
    
    parser.add_argument('-o', '--output', required=True)

    args = parser.parse_args()
    
    if not args.fn: 
        if not args.contact_file:
            parser.error("No data provided")
        else:
            # Parse Txt VCF file
            parseFromVCF(args.contact_file)

    
    vcf_prop            = vCardProperties()
    vcf_prop.fname      = args.fn
    vcf_prop.name       = args.n
    vcf_prop.weblist    = args.web
    vcf_prop.maillist   = args.email
    vcf_prop.tellist    = args.tel
    vcf_prop.region     = args.rg
    vcf_prop.country    = args.cn
    
    qr_prop             = QRCodeProperties()
    qr_prop.bgcolor     = args.bg
    qr_prop.fgcolor     = args.fg
    qr_prop.edcolor     = args.edgclr
    qr_prop.ctcolor     = args.cntclr
    qr_prop.stcolor     = args.strtclr
    qr_prop.endcolor    = args.endclr
        
    qr_prop.logo_path      =   args.logo
    qr_prop.logo_size      =   args.lgsz
    qr_prop.img_mask_path  =   args.imask
    qr_prop.shape          =   args.lshape
    qr_prop.color_mask     =   args.cmask
    qr_prop.img_type       =   args.img
    
    
    main(vcf_prop, qr_prop, args.output)
    
