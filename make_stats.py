import os
import cv2

def compute_aux (img1,img2, dominant):
	tp = 0
	tn  =0
	fp = 0
	fn = 0
	pozitives = 0
	negatives = 0
	for x in range (img2.shape[0]):
		for y in range (img2.shape[1]):
			if img1[x][y] >0:
				pozitives += 1	
				if img2[x][y] == dominant:
					tp +=1
				else:
					fn+=1
			if img1[x][y] ==0:
				negatives += 1
				if img2[x][y] == dominant:
					fp += 1
				else:
					tn += 1
	tp = tp / pozitives
	fn = fn / pozitives
	fp = fp / negatives
	tn = tn / negatives

	return (tp, fp, (tp+tn)/(tp+tn+fp+fn), tp/(tp+fp+fn))

def compute (img1, img2):
	colors = []
	for i in range(256):
		colors.append(0)
	for x in range (img2.shape[0]):
		for y in range (img2.shape[1]):
			if img1[x][y] >0:
				colors[img2[x][y]]+=1
	dominant1 = -1
	dominant2 = -1
	for i in range(256):
		if colors[i] > colors[dominant1]:
			dominant2 = dominant1
			dominant1 = i
		else:
			if colors[i] > colors[dominant2]:
				dominant2 = i
	#print (dominant1)
	#print (colors[dominant1])
	#print (dominant2)
	#print (colors[dominant2])
	tpd,fpd,accd,ioud = compute_aux(img1,img2, dominant1)
	tp,fp,acc,iou = compute_aux(img1,img2, dominant2)
	if iou > ioud:
		tpd = tp
		fpd = fp
		accd = acc
		ioud = iou		
		
	#print (tpd,fpd,accd,ioud)
	return (tpd,fpd,accd,ioud)
folder_init = "/home/david/Desktop/segm/"
folder_type = ["day", "dusk", "night"]
rezs = ["res1_ecnet/", "res_fcn/","res_pspnet/", "res_segnet/", "res_dilation/", "res_danet_512/", "res_danet_768/"]
counter = 0

fil = open ("results.txt","w")
for rez in rezs:
	TPR = 0
	FPR = 0
	ACC = 0
	IOU = 0
	COUNT = 0
	for extens in folder_type:
		TP_EXT = 0
		FP_EXT = 0
		ACC_EXT = 0
		IOU_EXT = 0
		folder = folder_init + extens
		counter = 0 
		for root, subdirs, files in os.walk(folder):
			for s1 in subdirs:
				if "rez" not in s1 and "res" not in s1:
					
					s2 = folder_init + rez + s1
					#print(s1)
					#print (s2)
					for r,s,f in os.walk(os.path.join(folder,s1) ):
                
						for img1 in f:
							if "frame" not in img1:
								#print(img1)
								img2 = s2 + "/" + "res1_" + img1[:-4]+ "-frame.png"
								img1 = folder + "/" + s1 + "/" + img1
								counter = counter + 1
								COUNT = COUNT + 1
								if counter % 10 ==0:
									print(counter)
								#print (img2) # output
								#print (img1) # ground truth
								img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
								img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
								img2 = cv2.resize(img2, (img1.shape[1],img1.shape[0]), interpolation = cv2.INTER_AREA)
								tp, fp, acc, iou = compute (img1, img2)
								TP_EXT += tp
								FP_EXT  += fp
								ACC_EXT += acc
								IOU_EXT += iou
								#fil.write("tp for method %s category %s is %lf" %(rez, extens, TP_EXT))
								
								#print ("tp for method %s category %s is %lf" %(rez, extens, TP_EXT))
								#print (img1.shape)
								#print (img2.shape)
								#cv2.imshow("i1",img1)
								#cv2.imshow("i2",img2)
								#cv2.waitKey(0)
								#cv2.destroyAllWindows()
		TPR += TP_EXT
		FPR += FP_EXT
		ACC += ACC_EXT
		IOU += IOU_EXT
								
		TP_EXT = (TP_EXT)/ counter
		FP_EXT = (FP_EXT)/ counter
		ACC_EXT =(ACC_EXT)/ counter
		IOU_EXT = (IOU_EXT)/ counter
		fil.write("tp for method %s category %s is %lf" %(rez, extens, TP_EXT))
		fil.write("fp for method %s category %s is %lf" %(rez, extens, FP_EXT))
		fil.write("acc for method %s category %s is %lf" %(rez, extens, ACC_EXT))
		fil.write("iou for method %s category %s is %lf" %(rez, extens, ACC_EXT))
		print("tp for method %s category %s is %lf" %(rez, extens, TP_EXT))
		print("fp for method %s category %s is %lf" %(rez, extens, FP_EXT))
		print("acc for method %s category %s is %lf" %(rez, extens, ACC_EXT))
		print("iou for method %s category %s is %lf" %(rez, extens, IOU_EXT))
		
	TPR/=COUNT
	FPR/=COUNT
	ACC/=COUNT
	IOU/=COUNT
	fil.write("average tp for method %s is %lf" %(rez, TPR))
	fil.write("average fp for method %s is %lf" %(rez,  FPR))					
	fil.write("average acc for method %s is %lf" %(rez, ACC))
	fil.write("average iou for method %s is %lf" %(rez, IOU))
	print("average tp for method %s is %lf" %(rez, TPR))
	print("average fp for method %s is %lf" %(rez,  FPR))					
	print("average acc for method %s is %lf" %(rez, ACC))
	print("average iou for method %s is %lf" %(rez, IOU))
			
fil.close()		
				
