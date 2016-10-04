import json
import re

j = open("output.prez.json")

breakPattern = '\n\tThursday, November 26, 2009 \n\t'
bp2 = '\n\tMarch 26, 2016 \n\t'
bp3 = '\n\tThe White House \n\tMarch 26, 2016 \n\t'
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

jp = json.load(j)

#patterns before speech:
#'\n\t Remarks of President Barack Obama as Delivered \n\tWeekly Address \n\tThe White House \n\tMarch 26, 2016 \n\t'
#'\n\t Remarks of President Barack Obama as Prepared for Delivery \n\tWeekly Address \n\tThe White House \n\tSeptember 10, 2016  \n\t'
#'\n\t Remarks of President Barack Obama \n\tWeekly Address \n\tNovember 14, 2009 \n\t'
# \n\t Video for President Barack Obama \n\tWeekly Address \n\tThe White House \n\tOctober 31, 2015 \n\t
#    Remarks of President Barack Obama \nWeekly Address \nThe White House \nAugust 22, 2015
# \n\t Remarks of President Barack Obama \n\t Weekly Address \n\t Lemont, Illinois \n\t March 16, 2013 \n\t

# \n\tRemarks of President Barack Obama Weekly Address October 17, 2009 \n\t \n\t

#'\n\t Remarks of President Barack Obama \n\tWeekly Address \n\tSaturday, November 21, 2009 \n\t'
#'\n\t Prepared Remarks of President Barack Obama \n\tWeekly Address \n\tThursday, November 26, 2009 \n\t'

# testing on the first entry:
'''
reStr = '[\n\t]*\s+(Video for)*(Prepared)*\s*(Remarks\s+of)*\s+President\s+Barack\s+Obama[\w\s]+\n\t*Weekly\s+Address\s+\n\t*([\w,\s]+\n\t\s+)*(The White House \n\t*)*[\w,\d\s]*\n\t*(.*)'
speechText = re.search(reStr, jp[0]['rawText'], re.DOTALL).group(4)
speechText = re.sub('\n\t', '', speechText).strip()
speechText = re.sub('#+', '', speechText).strip()
# testing on problem entries:
speechText = re.search(reStr, jp[6]['rawText'], re.DOTALL).group(4)
speechText = re.search(reStr, jp[9]['rawText'], re.DOTALL).group(5)
re.search(reStr, jp[13]['rawText'], re.DOTALL).group(5)
re.search(reStr, jp[-1]['rawText'], re.DOTALL)
re.search(reStr, jp[310]['rawText'], re.DOTALL)
re.search(reStr, jp[304]['rawText'], re.DOTALL)

re.search(reStr, jp[15]['rawText'], re.DOTALL) -- francine wheeler, not the prez
jp[17]['rawText']

'''
reStr = '[\n\t]*\s*(Video for)*(Prepared)*\s*(Remarks\s+of)*\s*President\s+Barack\s+Obama[\w\s]+\n*\t*Weekly\s+Address\s+\n*\t*([\w,\s]+\n\t\s+)*(The White House \n\t*)*[\w,\d\s]*[\n\t\s]*(.*)'
speechTexts = []
for i, e in enumerate(jp):
    if len(e['rawText']) < 1000:
        print 'speech text too short, skipping'
        continue
    speechRE = re.search(reStr, e['rawText'], re.DOTALL)
    if speechRE:
        speechText = speechRE.group(6)
        if i == 9:
            speechText = speechText[16:]
        speechText = re.sub('\n\t', '', speechText).strip()
        speechText = re.sub('#+', '', speechText).strip()
        speechTexts.append(speechText)
    else:
        print 'no match for', i

all = ' '.join(speechTexts)
# len(all.split(' '))# 96518 -- shakespear demo text is

all = '\r\n'.join(speechTexts)
with open('half_obama_weeklys.txt', 'w') as f:
    f.write(all)
