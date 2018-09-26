#!/usr/bin/env python
#encoding:utf8

import os,re,sys
import platform

from SilinHTML import SilinHTML

class silinCompare():
    def __init__(self,fileName1,fileName2):
        self.fileName1=fileName1
        self.fileName2=fileName2
        self.script_path=os.path.dirname(os.path.abspath(sys.argv[1]))

        self.judgePath()
        self.filelist=[]

        self.path=os.path.dirname(os.path.abspath(sys.argv[0]))
        self.init_html()

    def init_html(self):
        self.result_html=os.path.join(self.path,"result.html")
        if os.path.exists(self.result_html):
            os.remove(self.result_html)
        self.myHtml=SilinHTML(self.result_html)
        self.myHtml.html_header()

    def judgePath(self):
        if not os.path.exists(self.fileName1) or not os.path.exists(self.fileName2):
            print "Error:invaled arguments"
            sys.exit()
        if os.path.isdir(self.fileName1) and os.path.isdir(self.fileName2):
            self.isfiles=False
        elif os.path.isfile(self.fileName1) and os.path.isfile(self.fileName2):
            self.isfiles=True
        else:
            print "Error:invaled arguments"
            sys.exit()

    def readFiles(self,sourFile,destFile):
        '''读取文件，并删除 注释/* */  和 // '''
        with open(sourFile) as sf:
            lins1=sf.read()
        with open(destFile) as df:
            lins2=df.read()
        Rule1="(\/\*(\s|.)*?\*\/)|(\/\/.*)"
        lins1,lins2=self.erase_space(re.sub(Rule1,'',lins1),re.sub(Rule1,'',lins2))
        return lins1.strip(),lins2.strip()
        #return lins1,lins2
    def erase_space(self,Lins1,Lins2):
        '''删除多余的空格和多余的空行'''
        lins1=re.sub('\n\n*','\n',Lins1)
        lins2=re.sub('\n\n*','\n',Lins1)
        return re.sub(r'  +',' ',lins1),re.sub(r'  +',' ',lins2)
    
    def compareFiles(self,file1,file2):
        print "\n checking......\n"+file1+"\n"+file2
        if os.path.exists(file1) and os.path.exists(file2):
            lins1,lins2=self.readFiles(file1,file2)
        else:
            result=[file1,file2,'notExist']
            self.myHtml.WriteResult(result)
            return
        if lins1 == lins2:
            result=[file1,file2,'same']
        else:
            result=[file1,file2,'different']
        self.myHtml.WriteResult(result)

    def getFileList(self,dir,filelist):
        newDir=dir
        if os.path.isfile(dir):
            filelist.append(dir)
        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                newDir=os.path.join(dir,s)
                self.getFileList(newDir,filelist)
        return

    def compareALL(self):
        if self.isfiles:
            self.compareFiles(self.fileName1,self.fileName2)
        else:
            self.getFileList(self.fileName1,self.filelist)
            for i in self.filelist:
                if not os.path.splitext(i)[1] in ['.c','.v']:
                    continue    
                #if platform.system().lower()=="windows":
                #    self.compareFiles(i,os.path.join(self.fileName2,i.replace(self.fileName1+'\\','')))
                #else:
                self.compareFiles(i,os.path.join(self.fileName2,i.replace(self.fileName1,'')))
if __name__=='__main__':
    if len(sys.argv)!=3:
        print "Error:Please input the arguments"
        print "For Example:\n python SilinCompare.py file1 file2"
        sys.exit()
    sCompare=silinCompare(sys.argv[1],sys.argv[2])
    sCompare.compareALL()