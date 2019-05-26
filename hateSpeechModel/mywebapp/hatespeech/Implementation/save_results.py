import csv

import operator

import xlsxwriter


#TODO clean up this. Move to core maybe?

def evaluate(data,outputf,testfile,labels,model):
    """
    Ported from initial version. TODO refactor to accept new format of data and clean up this code
    :param data: array containing outputs in old format: [[prob_pred,pred_label,actual_label,text],...]
    :param outputf: output directory
    """
    filept=open(outputf+"/info_"+testfile.split("/")[-1].split(".")[0]+"_"+model+".csv", "w")
    filep=csv.writer(filept)
    filep.writerow(["Number of data-points ",len(data)])
    print ("Number of data-points: "+str(len(data)))
    filep.writerow(["Number of labels ",len(labels)])
    print ("Number of labels: "+str(len(labels)))
    perf=float(len([row[1] for row in data if row[1]==row[2]]))/float(len(data))
    
    filep.writerow(["Accuracy ",str(perf*100)+"%"])
    filep.writerow([])
    print ("Accuracy: "+str(perf*100)+"%\n")
    
    data.sort(key=operator.itemgetter(0),reverse=True)
    y_pred=[row[1] for row in data]
    y_true=[row[2] for row in data]

    for n in labels:
        tp=float(sum([(y_true[i]==n) and (y_pred[i]==n) for i in range(len(y_true))]))
        tn=float(sum([(y_true[i]!=n) and (y_pred[i]!=n) for i in range(len(y_true))]))
        fp=float(sum([(y_true[i]!=n) and (y_pred[i]==n) for i in range(len(y_true))]))
        fn=float(sum([(y_true[i]==n) and (y_pred[i]!=n) for i in range(len(y_true))]))
        #p=tp/(tp+fp)
        #r=tp/(tp+fn)
        #print "precision = ", p
        #print "recall = ", r
        #print "accuracy   =", ((tp+tn)/(tp+tn+fp+fn))*100
        if (tp+fp)==0:
            precision=0
        else:
            precision=(tp/(tp+fp))*100
        if (tp+fn)==0:
            recall=0
        else:
            recall=(tp/(tp+fn))*100
        fscore=(200*tp)/(2*tp+fp+fn)
        #fscore= ((p*r)/(p+r))*2*100
        filep.writerow(["Label ",n])
        filep.writerow(["F-score  ",str(fscore)+"%"])
        filep.writerow(["Precision  ",str(precision)+"%"])
        filep.writerow(["Recall  ",str(recall)+"%"])
        filep.writerow(["TP ",int(tp),"FP ",int(fp),"TN ",int(tn),"FN ",int(fn)])
        filep.writerow([])
        
        print ("F-score for label-"+str(n)+" is: "+str(fscore)+"%")
    filept.close()
    
    print ("Printing output file")
    with xlsxwriter.Workbook(outputf+"/output_"+testfile.split("/")[-1].split(".")[0]+"_"+model+'.xlsx') as workbook:
        worksheet = workbook.add_worksheet()
        row=0
        col=0
        worksheet.write(row, col, "probabilities")
        worksheet.write(row, col + 1, "predicted_labels")
        worksheet.write(row, col + 2, "actual_labels")
        worksheet.write(row, col + 3, "preprocessed_text")
        worksheet.write(row, col + 4, "original_text")
        
        for line in data:
            row+=1
            worksheet.write(row, col, line[0])
            worksheet.write(row, col + 1, line[1])
            worksheet.write(row, col + 2, line[2])
            worksheet.write(row, col + 3, line[3])
            worksheet.write(row, col + 4, line[4])
            
    print ("Printing misclassification file")  
    with xlsxwriter.Workbook(outputf+"/misclassification_"+testfile.split("/")[-1].split(".")[0]+"_"+model+'.xlsx') as workbook:
        worksheet = workbook.add_worksheet()
        row=0
        col=0
        worksheet.write(row, col, "probability")
        worksheet.write(row, col + 1, "predicted_label")
        worksheet.write(row, col + 2, "actual_label")
        worksheet.write(row, col + 3, "preprocessed_text")
        worksheet.write(row, col + 4, "original_text")
       
        for line in data:
            if line[1]!=line[2]:
                row+=1
                worksheet.write(row, col, line[0])
                worksheet.write(row, col + 1, line[1])
                worksheet.write(row, col + 2, line[2])
                worksheet.write(row, col + 3, line[3])
                worksheet.write(row, col + 4, line[4])

                


    """print ("Printing output file")
    with open(outputf+"/output_"+testfile.split("/")[-1].split(".")[0]+"_"+".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["y_predicted","y_actual","tweets"])
        for line in data:
            writer.writerow(line)

    print ("Printing misclassification file")
    with open(outputf+"/misclassification_"+testfile.split("/")[-1].split(".")[0]+"_"+".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["y_predicted","y_actual","tweets"])
        for line in data:
            if line[0]!=line[1]:
                writer.writerow(line)"""