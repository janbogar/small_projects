
import numpy as np
import colorsys as cs


def pixel_difference(col1, col2, threshold, select_criterion = "CRITERION_COMPOSITE"):
    """
    Direct reimplementation of gimp-2.6.8/app/core/gimpimage-contiguous-region.c.
    GIMP software is licensed under GPL.
    """

    if select_criterion == "CRITERION_COMPOSITE":
        max_ = np.max(np.abs(col1 - col2))
    elif select_criterion == "CRITERION_R":
        max_ = np.max(np.abs(col1[0] - col2[0]))
    elif select_criterion == "CRITERION_G":
        max_ = np.max(np.abs(col1[1] - col2[1]))
    elif select_criterion == "CRITERION_B":
        max_ = np.max(np.abs(col1[2] - col2[2]))
    elif select_criterion in ("CRITERION_H", "CRITERION_S", "CRITERION_V"):
        av0, av1, av2 = cs.rgb_to_hsv( *col1 )
        bv0, bv1, bv2 = cs.rgb_to_hsv( *col2 )
        if select_criterion == "CRITERION_H":
            dist1 = np.abs(av0 - bv0)
            dist2 = np.abs(av0 - 360 - bv0)
            dist3 = np.abs(av0 - bv0 + 360)
            max_ = np.min( (dist1, dist2) )
            if (max_ > dist3):
                max_ = dist3
        elif select_criterion == "CRITERION_S":
            max_ = np.abs(av1 - bv1)
        elif select_criterion == "CRITERION_V":
            max_ = np.abs(av2 - bv2)
    else:
        raise ValueError("Invalid select_criterion supplied!")

    if (max_ < threshold):
        return False
    else:
        return True

def get_mask(pixels, threshold, seed=(0,0), criterion = "CRITERION_COMPOSITE", bitness = 8, return_region = False):
    """
    Fill bounded region, based on an implementation by Eric S. Raymond:
    http://mail.python.org/pipermail/image-sig/2005-September/003559.html

    Licence unspecified, might count as public domain.
    """

    max_color = 2**bitness - 1
    #threshold *= 1./max_color
    x, y = seed

    mask=np.full((pixels.shape[0],pixels.shape[1]), True, dtype='bool')
    mask[x,y]=False

    # Color normalization, so that the colors are in the range [0, 1]
    def normalize (color):
        return np.true_divide(color, max_color)
    
    # Get and normalize the color of the seed point
    seed_normalized = normalize(pixels[x, y])

    edge = [ (x, y) ]
    while edge:
        newedge = []
        for (x, y) in edge:
            #print x,y
            for (s, t) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if mask[s,t]:
                    try:
                        pix = pixels[s, t]
                    except IndexError:
                        pass
                    else:
                        if not pixel_difference(seed_normalized, normalize(pix), threshold, criterion) and np.any(mask):
                            mask[s, t] = False
                            newedge.append((s, t))
                            
        edge = newedge

    return mask

if __name__=='__main__':
    from PIL import Image
    import cStringIO
    import json
    import urllib2
    import matplotlib.pyplot as plt
    
    inputfile=open('images.jsonl')

    def parseline(line):
        try:
            return json.loads(line)
        except:
            return None
        
    def get_image(scraped):
        try:
            #sleep(1)
            print 'loading ',scraped['img']
            return urllib2.urlopen(scraped['img']).read()
        except:
            print 'failed, moving on'
            return None
    
    for i in range(10):
        line=inputfile.readline().strip()
        scraped=parseline(line)
        imgdata=get_image(scraped)        

        img=Image.open(cStringIO.StringIO(imgdata))
        img.show()

        img_array=np.asarray(img)
        print 'going for it'
        mask=get_mask(img_array,threshold=0.1)
        print 'done'

        plt.imshow(mask,interpolation='nearest')
        plt.show()
        raw_input('hit enter or whatever')      
