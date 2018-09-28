#!/usr/bin/env python
#encoding:utf8

import os,re,sys
import platform,difflib

from SilinHTML import SilinHTML

class silinCompare():
    def __init__(self,fileName1,fileName2):
        self.fileName1=os.path.abspath(fileName1)
        self.fileName2=os.path.abspath(fileName2)

        self.judgePath()
        self.filelist=[]

        self.path=os.path.dirname(os.path.abspath(sys.argv[0]))
        self.init_html()
        self.judgeSYS()
        self.init_log()
        self.diff=difflib.HtmlDiff()
        self.fileTag=['.c','.v','.h']
    def judgeSYS(self):
        if platform.system().lower()=="windows":
            self.SYStag='\\'
        else:
            self.SYStag='/'
    def init_log(self):
        self.logPath=os.path.join(self.path,"Silinhtml")
        if not os.path.exists(self.logPath):
            os.mkdir(self.logPath)

    def init_html(self):
        self.result_html=os.path.join(self.path,"result.html")
        if os.path.exists(self.result_html):
            os.remove(self.result_html)
        self.myHtml=SilinHTML(self.result_html)
        self.myHtml.html_header(self.fileName1,self.fileName2)

    def judgePath(self):
        if not os.path.exists(self.fileName1) or not os.path.exists(self.fileName2):
            print "Error:invaled arguments"
            sys.exit()
        if os.path.isdir(self.fileName1) and os.path.isdir(self.fileName2):
            self.isdirs=True
        elif os.path.isfile(self.fileName1) and os.path.isfile(self.fileName2):
            self.isdirs=False
            self.fileName1,self.filelist[0]=os.path.split(self.fileName1)
            self.fileName2,self.filelist[1]=os.path.split(self.fileName2)
        else:
            print "Error:invaled arguments"
            sys.exit()

    def readFiles(self,sourFile,destFile):
        '''读取文件，并删除 注释/* */  和 // '''
        with open(sourFile) as sf:
            lins1=sf.read()
        with open(destFile) as df:
            lins2=df.read()
        Rule1="(\/\*(\s|.)*?\*\/)|(\/\/.*)|\r|\t"
        lins1,lins2=self.erase_space(re.sub(Rule1,'',lins1),re.sub(Rule1,'',lins2))
        if len(lins1)>0 and lins1[0]=="":
            del lins1[0]
        if len(lins2)>0 and lins2[0]=="":
            del lins2[0]    
        return lins1,lins2
        #return lins1,lins2
    def erase_space(self,Lins1,Lins2):
        '''删除多余的空格和多余的空行'''
        lins1=re.sub('\n(\n| )*','\n',Lins1)
        lins2=re.sub('\n(\n| )*','\n',Lins1)
        
        lins1=re.sub(r'  +',' ',lins1).splitlines()
        lins2=re.sub(r'  +',' ',lins2).splitlines()

        lins1='\n'.join([x.strip() for x in lins1])
        lins2='\n'.join([x.strip() for x in lins2])

        return lins1.splitlines(),lins2.splitlines()
    
    def compareFiles(self,file1,file2,inde,files):
        print "\n checking......\n"+file1+"\n"+file2
        if not os.path.exists(file1):
            result=['',files,'notExist','']
            self.myHtml.WriteResult(result)
            return
        elif not os.path.exists(file2):
            result=[files,'','notExist','']
            self.myHtml.WriteResult(result)
            return
        elif os.path.exists(file1) and os.path.exists(file2):
            lins1,lins2=self.readFiles(file1,file2)
        htmlPath=os.path.join(self.logPath,str(inde)+'.html')
        result=[files,files,'',htmlPath]
        if lins1 == lins2:
            result[2]='same'
        else:
            result[3]='different'
        self.myHtml.WriteResult(result)
        with open(htmlPath,'w') as f:
            f.write(self.diff.make_file(lins1,lins2))
        return

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
        inde=0
        if self.isdirs:
            self.getFileList(self.fileName1,self.filelist)
            self.getFileList(self.fileName2,self.filelist)
            self.filelist=[x.replace(self.fileName1+self.SYStag,'') for x in self.filelist]
            self.filelist=[x.replace(self.fileName2+self.SYStag,'') for x in self.filelist]
            self.filelist=list(set(self.filelist))
        for i in self.filelist:
            inde +=1
            if not os.path.splitext(i)[1] in self.fileTag:
                    continue        
            self.compareFiles(os.path.join(self.fileName1,i),os.path.join(self.fileName2,i),inde,i)
if __name__=='__main__':
    if len(sys.argv)!=3:
        print "Error:Please input the arguments"
        print "For Example:\n python SilinCompare.py file1 file2"
        sys.exit()
    sCompare=silinCompare(sys.argv[1],sys.argv[2])
    sCompare.compareALL()