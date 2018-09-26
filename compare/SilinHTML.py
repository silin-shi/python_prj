#!/usr/bin/env python
#encoding:utf8

import sys,os,time,re
import json

class SilinHTML():
    def __init__(self,result_html):
        self.html=result_html
    
    def html_header(self):
        HtmlHeader='''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width,initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>执行结果</title>
            <style>
                body{
                    font-size:14px;
                }
                table{
                    font-family:verdana,arial,sans-serif;
                    font-size:11px;
                    color:#333333;
                    border-width:1px;
                    border-color:#666666;
                    border-collapse:collapse;
                }
                table th {
                    border-width:1px;
                    padding:8px;
                    border-style:solid;
                    border-color:#666666;
                    background-color:#B7D3F6;
                }
                table td{
                    border-width:1px;
                    padding:8px;
                    border-style:solid;
                    border-color:#666666;
                    background-color:#ffffff;
                }
                .result {

                }
                .same,.Same,.SAME{
                    color:#1c6194;
                    background-color:#5ce665;
                }
                .notExist,.UNKNOWN,.unknown{
                    color:#bf5ebb;
                    background-color:#efdb12;
                }
                .different,.Different,.DIFFERENT{
                    color:#fbf8fb;
                    background-color:#f76d6f;
                }
            </style>
        </head>
        <body>
            <table>
                <thead>
                    <tr>
                        <th>file1</th> 
                        <th>file2</th>
                        <th>结果</th>  
                    </tr>
                </thead>
                <tbody>
        '''
        self.WriteToHtml(HtmlHeader)
    def html_bottom(self):
        HtmlBottom='''
        </tbody>
        </table>
        </body>
        </html>
        '''
        self.WriteToHtml(HtmlBottom)
    def WriteResult(self,result):
        tds='\n<tr><td>%s</td><td>%s</td><td class=%s>%s</td></tr>' %(result[0],result[1],result[2],result[2])
        self.WriteToHtml(tds)

    def WriteToHtml(self,Connect):
        with open(self.html,"a") as f:
            f.write(Connect)