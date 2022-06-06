# import modules
import qrcode
from PIL import Image
import vobject
from qrcode.image.styledpil import *
from qrcode.image.svg import *
# from qrcode.image.pure import *
from qrcode.image.styles.moduledrawers import *
from qrcode.image.styles.colormasks import *
import argparse


class vCardProperties():
    def __init__(self):
        self.fname = None
        self.name  = None
        self.weblist  = []
        self.maillist = []
        self.tellist  = []
        self.region   = ''
        self.country  = ''

class QRCodeProperties():
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
        

clr_hex_to_tuple = lambda x : (int(x[1:3],16),int(x[3:5],16),int(x[5:],16))

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
    
    for tl in vCardProp.tellist:
        vCrd.add('tel').value = tl
 
    # adding URL or text to QRcode
    QRcode.add_data(vCrd.serialize())
 
    # generating QR code
    QRcode.make(fit=True)

    img_fctry = {
                'StyledPNG' : StyledPilImage,
                # 'PurePNG'   : PymagingImage,
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
    
    fgclr       =   clr_hex_to_tuple(QRProp.fgcolor)  if QRProp.fgcolor.startswith('#') else QRProp.fgcolor
    bgclr       =   clr_hex_to_tuple(QRProp.bgcolor)  if QRProp.bgcolor.startswith('#') else QRProp.bgcolor
    strtclr     =   clr_hex_to_tuple(QRProp.stcolor)  if QRProp.stcolor.startswith('#') else QRProp.stcolor
    endclr      =   clr_hex_to_tuple(QRProp.endcolor) if QRProp.endcolor.startswith('#') else QRProp.endcolor

    clr_msk_prms =  {
                'SolidFill'             : dict(back_color = bgclr, front_color = fgclr),
                'RadialGradiant'        : dict(back_color = bgclr, center_color= strtclr, edge_color  = endclr),
                'SquareGradiant'        : dict(back_color = bgclr, center_color= strtclr, edge_color  = endclr),
                'HorizontalGradiant'    : dict(back_color = bgclr, left_color  = strtclr, right_color = endclr),
                'VerticalGradiant'      : dict(back_color = bgclr, top_color   = strtclr, bottom_color= endclr),
                'Image'                 : dict(back_color = bgclr, color_mask_path = QRProp.img_mask_path)
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
                           color_mask=clr_msk[QRProp.color_mask](**clr_msk_prms[QRProp.color_mask])
                         ).convert('RGB')
    
    if QRProp.logo_path:
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)

        QRimg.paste(logo, pos)

    # save the QR code generated
    QRimg.save(outfile)

def parseFromVCF(vcf_file_path):
    pass

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='')
    
    # Data Fields
    parser.add_argument('-fn',      '--formatted_name',     help='Display Name for vCard')
    parser.add_argument('-n',       '--name',               default='', help='Actual Name for vCard')
    parser.add_argument('-web',     '--website',            default=[], help='Personal Website',    action='extend', nargs='*')
    parser.add_argument('-email',   '--email',              default=[], help='Email for vCard',     action='extend', nargs='*')
    parser.add_argument('-tel',     '--telephone',          default=[], help='Telephone No.',       action='extend', nargs='*')
    parser.add_argument('-rg',      '--region',             default='', help='Region of residence')
    parser.add_argument('-cn',      '--country',            default='', help='Country of residence')
    
    # Or pick data from vcf (.txt) file
    parser.add_argument('-vf',      '--contact_file',       help='Use text file containing data in standard VCF format')
    
    # QR Customisation
    parser.add_argument('-bg',      '--back_color',         default='#ffffff',    help='Background Color')
    parser.add_argument('-fg',      '--fore_color',         default='#000000',    help='Foreground Color')
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
                        choices = ['StyledPNG', 'SVG'], #, 'PurePNG'],
                        help='End Color for Horizontal/Vertical Gradient')
    # PymagingImage : PNG without QR customisations
    # StyledPIL     : PNG with QR customisations
    
    # parser.add_argument('-edgclr',  '--edge_color',         default='#000000',    help='Edge Color for Radial Gradient')
    # parser.add_argument('-cntclr',  '--center_color',       default='#000000',    help='Center Color for Radial Gradient')
    parser.add_argument('-strtclr', '--start_color',        default='#ff00ff',    help='Start Color for Horizontal/Vertical Gradient')
    parser.add_argument('-endclr',  '--end_color',          default='#00ffff',    help='End Color for Horizontal/Vertical Gradient')
    
    parser.add_argument('-imask',    '--image_mask_path',   default=None,       help='Use mentioned image as foreground color in QR code')
    
    parser.add_argument('-o', '--output', required=True)

    args = parser.parse_args()
    
    if not args.formatted_name:
        if not args.contact_file:
            parser.error("No data provided")
        else:
            # Parse Txt VCF file
            parseFromVCF(args.contact_file)

    vcf_prop            = vCardProperties()
    vcf_prop.fname      = args.formatted_name
    vcf_prop.name       = args.name
    vcf_prop.weblist    = args.website
    vcf_prop.maillist   = args.email
    vcf_prop.tellist    = args.telephone
    vcf_prop.region     = args.region
    vcf_prop.country    = args.country
    
    qr_prop             = QRCodeProperties()
    qr_prop.bgcolor     = args.back_color
    qr_prop.fgcolor     = args.fore_color
    # qr_prop.edcolor     = args.edgclr
    # qr_prop.ctcolor     = args.cntclr
    qr_prop.stcolor     = args.start_color
    qr_prop.endcolor    = args.end_color
        
    qr_prop.logo_path      =   args.logo_path
    qr_prop.logo_size      =   args.logo_size
    qr_prop.img_mask_path  =   args.image_mask_path
    qr_prop.shape          =   args.line_shape
    qr_prop.color_mask     =   args.color_mask
    qr_prop.img_type       =   args.image_type
    
    
    main(vcf_prop, qr_prop, args.output)
    
