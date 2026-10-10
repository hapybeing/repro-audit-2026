library(foreign)
library(ggplot2)
library(dplyr)
library(tidytext)
library(lubridate)
library(readr)
library(scales)
library(broom)
library(httr)
library(rtweet)
library(ggeffects)
library(ggpubr)
library(devtools)
library(stringr)
library(rio)
library(eeptools)
theme_set(theme_pubr())

load("StateLeg_COVIDFacebookActivity.Rdata")

#remove Independents and POC Republicans due to small sample sizes
table(by_leg$rpg)
by_leg2=subset(by_leg,rpg !="Independent White Men" & rpg !="Republican Men of Color" & rpg !="Republican Women of Color")
table(by_leg2$rpg)
by_leg2$rpg=factor(by_leg2$rpg,levels = c("Republican White Men","Democratic White Men","Republican White Women","Democratic White Women","Democratic Men of Color","Democratic Women of Color"))
table(by_leg2$rpg)

by_leg2$rpg2=factor(by_leg2$rpg,levels = c("Democratic White Women","Republican White Men","Democratic White Men","Republican White Women","Democratic Men of Color","Democratic Women of Color"))

                                         ####################By Race & Gender######################

basics= by_leg %>% 
  group_by(poc)  %>% 
  summarize(total=sum(general),mean_total=mean(general),covid=sum(covid),testing=sum(testing),sd=sum(sd),events=sum(event),partisan=sum(partisan),gender=sum(gender),racial=sum(racial),budget=sum(budget),all_sd=sum(all_sd),non_covid_sd=sum(non_covid_sd))

basics$prop_covid=basics$covid/basics$total
basics$prop_testing=basics$testing/basics$total
basics$prop_sd=basics$sd/basics$total
basics$prop_events=basics$events/basics$total
basics$prop_partisan=basics$partisan/basics$total
basics$prop_gender=basics$gender/basics$total
basics$prop_racial=basics$racial/basics$total
basics$prop_budget=basics$budget/basics$total
basics$prop_all_sd=basics$all_sd/basics$total
basics$prop_non_covid_sd=basics$non_covid_sd/basics$total


basics$freq=c(335,101,114,104)
basics$Group= c("White Men (n=335)","White Women (n=101)","Men of Color (n=114)","Women of Color (n=104)")
basics$Group=factor(basics$Group,levels = c("White Men (n=335)","White Women (n=101)","Men of Color (n=114)","Women of Color (n=104)"))
basics$group3= c("White Men","White Women","Men of Color","Women of Color")
basics$group3=factor(basics$group3,levels = c("White Men","White Women","Men of Color","Women of Color"))

#Proportions
#General Frequency Plots 

p1=ggplot(data = basics, aes(x=group3, y=total))+
 geom_bar(stat="identity")+
  geom_text(aes(label=total), hjust=1.6, color="white", size=3)+
  theme_minimal()+ggtitle("All") +
  ylab("# of Total Posts") +xlab("") +coord_flip()


p2=ggplot(data = basics, aes(x=group3, y=prop_covid*100))+
 geom_bar(stat="identity") +ggtitle("COVID") +
  geom_text(aes(label=percent(prop_covid,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()


p3=ggplot(data = basics, aes(x=group3, y=prop_testing*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Dangers") +
  geom_text(aes(label=percent(prop_testing,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()

p4=ggplot(data = basics, aes(x=group3, y=prop_sd*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Social Distancing") +
  geom_text(aes(label=percent(prop_sd,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()

p5=ggplot(data = basics, aes(x=group3, y=prop_events*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Events") +
  geom_text(aes(label=percent(prop_events,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()

p6=ggplot(data = basics, aes(x=group3, y=prop_partisan*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Partisan") +
  geom_text(aes(label=percent(prop_partisan,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()


p7=ggplot(data = basics, aes(x=group3, y=prop_gender*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Women") +
  geom_text(aes(label=percent(prop_gender,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()


p8=ggplot(data = basics, aes(x=group3, y=prop_racial*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Race") +
  geom_text(aes(label=percent(prop_racial,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()

p9=ggplot(data = basics, aes(x=group3, y=prop_budget*100))+
 geom_bar(stat="identity")+ggtitle("Budget") +
  geom_text(aes(label=percent(prop_budget,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()


together <- ggarrange(p2,p3, p4,p5,p6,p7,p8,p9, ncol = 2, nrow = 4,common.legend = TRUE, font.label = list(size=12),vjust = .5)
ggexport(together,filename = "Total Activity Analysis_RaceAndGender/Percent_covid_dangers_sd_event_partisan_gender_race_budget.pdf",height =5,width = 6 )


library(xtable)
print(xtable(basics),type="html",file="Total Activity Analysis_RaceAndGender/totalsandprops.doc")

names(basics)
basics2=basics[,c(25,2,4:11)]
colnames(basics2)=c("","All","COVID","COVID-Dangers","COVID-Social Distancing","COVID-Events","COVID-Partisan","COVID-Women","COVID-Race","Budget")
print(xtable(basics2),type="html",file="Total Activity Analysis_RaceAndGender/sumsbyraceandgender.doc")


                                     ######################By Race, Gender, and Party######################

basics= by_leg2 %>% 
  group_by(rpg)  %>% 
  summarize(total=sum(general),mean_total=mean(general),covid=sum(covid),testing=sum(testing),sd=sum(sd),events=sum(event),partisan=sum(partisan),gender=sum(gender),racial=sum(racial),budget=sum(budget),all_sd=sum(all_sd),non_covid_sd=sum(non_covid_sd))

basics$prop_covid=basics$covid/basics$total
basics$prop_testing=basics$testing/basics$total
basics$prop_sd=basics$sd/basics$total
basics$prop_events=basics$events/basics$total
basics$prop_partisan=basics$partisan/basics$total
basics$prop_gender=basics$gender/basics$total
basics$prop_racial=basics$racial/basics$total
basics$prop_budget=basics$budget/basics$total
basics$prop_all_sd=basics$all_sd/basics$total
basics$prop_non_covid_sd=basics$non_covid_sd/basics$total


basics$freq=c(242,91,38,63,108,101)
basics$Group= c("Republican White Men (n=242)","Democratic White Men (n=91)","Republican White Women (n=38)","Democratic White Women (n=63)","Democratic Men of Color (n=108)","Democratic Women of Color (n=101)")
basics$Group=factor(basics$Group,levels= c("Republican White Men (n=242)","Democratic White Men (n=91)","Republican White Women (n=38)","Democratic White Women (n=63)","Democratic Men of Color (n=108)","Democratic Women of Color (n=101)"))
basics$group2=rownames(basics)
basics$group3= c("Republican White Men","Democratic White Men","Republican White Women","Democratic White Women","Democratic Men of Color","Democratic Women of Color")
basics$group3=factor(basics$group3,levels =c("Republican White Men","Democratic White Men","Republican White Women","Democratic White Women","Democratic Men of Color","Democratic Women of Color") )

#Proportions
#General Frequency Plots 
p1=ggplot(data = basics, aes(x=group3, y=total))+
 geom_bar(stat="identity")+
  geom_text(aes(label=total), hjust=1.6, color="white", size=3)+
  theme_minimal()+ggtitle("All") +
  ylab("# of Total Posts") +xlab("") +coord_flip()


p2=ggplot(data = basics, aes(x=group3, y=prop_covid*100))+
 geom_bar(stat="identity") +ggtitle("COVID") +
  geom_text(aes(label=percent(prop_covid,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()


p3=ggplot(data = basics, aes(x=group3, y=prop_testing*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Dangers") +
  geom_text(aes(label=percent(prop_testing,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()

p4=ggplot(data = basics, aes(x=group3, y=prop_sd*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Social Distancing") +
  geom_text(aes(label=percent(prop_sd,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()

p5=ggplot(data = basics, aes(x=group3, y=prop_events*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Events") +
  geom_text(aes(label=percent(prop_events,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()

p6=ggplot(data = basics, aes(x=group3, y=prop_partisan*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Partisan") +
  geom_text(aes(label=percent(prop_partisan,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()


p7=ggplot(data = basics, aes(x=group3, y=prop_gender*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Women") +
  geom_text(aes(label=percent(prop_gender,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()


p8=ggplot(data = basics, aes(x=group3, y=prop_racial*100))+
 geom_bar(stat="identity")+ggtitle("COVID-Race") +
  geom_text(aes(label=percent(prop_racial,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()

p9=ggplot(data = basics, aes(x=group3, y=prop_budget*100))+
 geom_bar(stat="identity")+ggtitle("Budget") +
  geom_text(aes(label=percent(prop_budget,accuracy = .1)), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("% of Total Posts")+xlab("")+coord_flip()


together <- ggarrange(p2,p3, p4,p5,p6,p7,p8,p9, ncol = 2, nrow = 4,common.legend = TRUE, font.label = list(size=12),vjust = .5)
ggexport(together,filename = "Total Activity Analysis_RaceAndGenderAndParty_v1/Percent_covid_dangers_sd_event_partisan_gender_race_budget.pdf",height =5,width = 6 )


library(xtable)
print(xtable(basics),type="html",file="Total Activity Analysis_RaceAndGenderAndParty_v1/totalsandprops.doc")

names(basics)
basics2=basics[,c(25,2,4:11)]
colnames(basics2)=c("","All","COVID","COVID-Dangers","COVID-Social Distancing","COVID-Events","COVID-Partisan","COVID-Women","COVID-Race","Budget")
print(xtable(basics2),type="html",file="Total Activity Analysis_RaceAndGenderAndParty_v1/sumsbyraceandgenderandparty.doc")

                                          ######################By Race & Gender######################
#Checking for signifigance
summary(aov(general~poc, data = by_leg)) #Standard ANOVA

#Difference of Means Across Race-Gender Groups
TukeyHSD(aov(general~poc, data = by_leg)) #Multiple pair wise test
TukeyHSD(aov(covid~poc, data = by_leg)) #Multiple pair wise test

#Compares Means of White Men to all Non-White Mean
t.test(by_leg$general[by_leg$poc=="White Man"],by_leg$general[by_leg$poc!="White Man"]) #Significant

table(by_leg$poc)
basics= by_leg %>% 
  group_by(poc)  %>% 
  summarize(average_total=round(mean(general)),average_covid=round(mean(covid)),average_testing=round(mean(testing)),average_sd=round(mean(sd)),average_events=round(mean(event)),average_partisan=round(mean(partisan)),average_gender=round(mean(gender)),average_racial=round(mean(racial)),average_budget=round(mean(budget)),average_all_sd=round(mean(all_sd)),average_non_covid_sd=round(mean(non_covid_sd)))

basics$freq=c(335,101,114,104)
basics$Group= c("White Men (n=335)","White Women (n=101)","Men of Color (n=114)","Women of Color (n=104)")
basics$Group=factor(basics$Group,levels = c("White Men (n=335)","White Women (n=101)","Men of Color (n=114)","Women of Color (n=104)"))
basics$group3= c("White Men","White Women","Men of Color","Women of Color")
basics$group3=factor(basics$group3,levels = c("White Men","White Women","Men of Color","Women of Color"))


#Averages
#General Frequency Plots 
p1=ggplot(data = basics, aes(x=group3, y=average_total))+
 geom_bar(stat="identity")+
  geom_text(aes(label=average_total), hjust=1.6, color="white", size=3)+
  theme_minimal()+ggtitle("All") +
  ylab("Mean # of Posts") +xlab("") +coord_flip()


p2=ggplot(data = basics, aes(x=group3, y=average_covid))+
 geom_bar(stat="identity") +
  geom_text(aes(label=average_covid), hjust=1.6, color="white", size=3)+
  theme_minimal()+ ggtitle("COVID") +
  ylab("Mean # of Posts")+xlab("")+coord_flip()


p3=ggplot(data = basics, aes(x=group3, y=average_testing))+
 geom_bar(stat="identity")+ggtitle("COVID-Dangers") +
  geom_text(aes(label=average_testing), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

p4=ggplot(data = basics, aes(x=group3, y=average_sd))+
 geom_bar(stat="identity")+ggtitle("COVID-Social Distancing") +
  geom_text(aes(label=average_sd), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

p5=ggplot(data = basics, aes(x=group3, y=average_events))+
 geom_bar(stat="identity")+ggtitle("COVID-Events") +
  geom_text(aes(label=average_events), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

p6=ggplot(data = basics, aes(x=group3, y=average_partisan))+
 geom_bar(stat="identity")+ggtitle("COVID-Partisan") +
  geom_text(aes(label=average_partisan), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()


p7=ggplot(data = basics, aes(x=group3, y=average_gender))+
 geom_bar(stat="identity")+ggtitle("COVID-Women") +
  geom_text(aes(label=average_gender), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()


p8=ggplot(data = basics, aes(x=group3, y=average_racial))+
 geom_bar(stat="identity")+ggtitle("COVID-Race") +
  geom_text(aes(label=average_racial), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

p9=ggplot(data = basics, aes(x=group3, y=average_all_sd))+
 geom_bar(stat="identity")+ggtitle("Social Distancing") +
  geom_text(aes(label=average_all_sd), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

p10=ggplot(data = basics, aes(x=group3, y=average_non_covid_sd))+
 geom_bar(stat="identity")+ggtitle("Non-COVID Social Distancing") +
  geom_text(aes(label=average_non_covid_sd), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()


together <- ggarrange(p1, p2, ncol = 2, nrow = 1,common.legend = TRUE, font.label = list(size=12),vjust = .5)
ggexport(together,filename = "Total Activity Analysis_RaceAndGender/Averagesbyraceandgender_total_and_covid_only.pdf",height =3,width = 6)

ggexport(p2,filename = "Total Activity Analysis_RaceAndGender/Averagesbyraceandgender_covid_only.pdf",height =3,width = 6)

together <- ggarrange(p3, p4,p5,p6,p7,p8, ncol = 2, nrow = 3,common.legend = TRUE, font.label = list(size=12),vjust = .5)
ggexport(together,filename = "Total Activity Analysis_RaceAndGender/Averages_dangers_sd_event_partisan_gender_race.pdf",height =5,width = 6 )

library(xtable)
print(xtable(basics),type="html",file="Total Activity Analysis_RaceAndGender/totalsandmeans.doc")

names(basics)
basics2=basics[,c(14,2:10)]
colnames(basics2)=c("","All","COVID","COVID-Dangers","COVID-Social Distancing","COVID-Events","COVID-Partisan","COVID-Women","COVID-Race","Budget")
print(xtable(basics2),type="html",file="Total Activity Analysis_RaceAndGender/meansbyraceandgender.doc")



                       ######################By Race, Gender, and Party without GOP MOC and GOP WOC ######################

table(by_leg2$rpg)
basics= by_leg2 %>% 
  group_by(rpg)  %>% 
summarize(average_total=round(mean(general)),average_covid=round(mean(covid)),average_testing=round(mean(testing)),average_sd=round(mean(sd)),average_events=round(mean(event)),average_partisan=round(mean(partisan)),average_gender=round(mean(gender)),average_racial=round(mean(racial)),average_budget=round(mean(budget)),average_all_sd=round(mean(all_sd)),average_non_covid_sd=round(mean(non_covid_sd)))


TukeyHSD(aov(general~rpg, data = by_leg2)) #Multipple pair wise test
TukeyHSD(aov(covid~rpg, data = by_leg2)) #Multipple pair wise test
TukeyHSD(aov(sd~rpg, data = by_leg2)) #Multipple pair wise test
TukeyHSD(aov(event~rpg, data = by_leg2)) #Multipple pair wise test
TukeyHSD(aov(partisan~rpg, data = by_leg2)) #Multipple pair wise test
TukeyHSD(aov(gender~rpg, data = by_leg2)) #Multipple pair wise test
TukeyHSD(aov(racial~rpg, data = by_leg2)) #Multipple pair wise test
TukeyHSD(aov(all_sd~rpg, data = by_leg2)) #Multipple pair wise test
TukeyHSD(aov(non_covid_sd~rpg, data = by_leg2)) #Multipple pair wise test



t.test(by_leg2$budget[by_leg2$rpg=="Democratic Women of Color" | by_leg2$rpg=="Democratic Men of Color" |by_leg2$rpg=="Democratic White Women" |by_leg2$rpg=="Democratic White Men"],by_leg2$budget[by_leg2$rpg=="Republican White Men"])


table(by_leg2$rpg)
table(by_leg2$poc)

by_leg2$Legislator[by_leg2$GOP!= by_leg2$Republican]


basics$freq=c(242,91,38,63,108,101)
basics$Group= c("Republican White Men (n=242)","Democratic White Men (n=91)","Republican White Women (n=38)","Democratic White Women (n=63)","Democratic Men of Color (n=108)","Democratic Women of Color (n=101)")
basics$Group=factor(basics$Group,levels= c("Republican White Men (n=242)","Democratic White Men (n=91)","Republican White Women (n=38)","Democratic White Women (n=63)","Democratic Men of Color (n=108)","Democratic Women of Color (n=101)"))
basics$group2=rownames(basics)
basics$group3= c("Republican White Men","Democratic White Men","Republican White Women","Democratic White Women","Democratic Men of Color","Democratic Women of Color")
basics$group3=factor(basics$group3,levels =c("Republican White Men","Democratic White Men","Republican White Women","Democratic White Women","Democratic Men of Color","Democratic Women of Color") )



#Averages
#General Frequency Plots 
p1=ggplot(data = basics, aes(x=group3, y=average_total))+
 geom_bar(stat="identity")+
  geom_text(aes(label=average_total), hjust=1.6, color="white", size=3)+
  theme_minimal()+ggtitle("All") +
  ylab("Mean # of Posts") +xlab("") +coord_flip()


p2=ggplot(data = basics, aes(x=group3, y=average_covid))+
 geom_bar(stat="identity") +
  geom_text(aes(label=average_covid), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()+ggtitle("COVID")

p3=ggplot(data = basics, aes(x=group3, y=average_testing))+
 geom_bar(stat="identity")+ggtitle("COVID-Dangers") +
  geom_text(aes(label=average_testing), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()


p4=ggplot(data = basics, aes(x=group3, y=average_sd))+
 geom_bar(stat="identity")+ggtitle("COVID-Social Distancing") +
  geom_text(aes(label=average_sd), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

p5=ggplot(data = basics, aes(x=group3, y=average_events))+
 geom_bar(stat="identity")+ggtitle("COVID-Events") +
  geom_text(aes(label=average_events), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

p6=ggplot(data = basics, aes(x=group3, y=average_partisan))+
 geom_bar(stat="identity")+ggtitle("COVID-Partisan") +
  geom_text(aes(label=average_partisan), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()


p7=ggplot(data = basics, aes(x=group3, y=average_gender))+
 geom_bar(stat="identity")+ggtitle("COVID-Women") +
  geom_text(aes(label=average_gender), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

p8=ggplot(data = basics, aes(x=group3, y=average_racial))+
 geom_bar(stat="identity")+ggtitle("COVID-Race") +
  geom_text(aes(label=average_racial), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

p9=ggplot(data = basics, aes(x=group3, y=average_all_sd))+
 geom_bar(stat="identity")+ggtitle("All Social Distancing") +
  geom_text(aes(label=average_all_sd), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

p10=ggplot(data = basics, aes(x=group3, y=average_non_covid_sd))+
 geom_bar(stat="identity")+ggtitle("Non-COVID Social Distancing") +
  geom_text(aes(label=average_non_covid_sd), hjust=1.6, color="white", size=3)+
  theme_minimal()+ 
  ylab("Mean # of Posts")+xlab("")+coord_flip()

together <- ggarrange(p1, p2, ncol = 2, nrow = 1,common.legend = TRUE, font.label = list(size=12),vjust = .5)
ggexport(together,filename = "Total Activity Analysis_RaceAndGenderAndParty_v1/Averagesbyraceandgenderandparty_total_and_covid_only.pdf",height =3,width = 6)

ggexport(p2,filename = "Total Activity Analysis_RaceAndGenderAndParty_v1/Averagesbyraceandgenderandparty_covid_only.pdf",height =3,width = 6)

together <- ggarrange(p3,p4,p5,p6,p7,p8, ncol = 2, nrow = 3,common.legend = TRUE, font.label = list(size=12),vjust = .5)
ggexport(together,filename = "Total Activity Analysis_RaceAndGenderAndParty_v1/Averages_dangers_sd_event_partisan_gender_race.pdf",height =6,width = 8 )

together <- ggarrange(p4,p8,p9, ncol = 2, nrow = 2,common.legend = TRUE, font.label = list(size=12),vjust = .5)
ggexport(together,filename = "Total Activity Analysis_RaceAndGenderAndParty_v1/Comparing Social Distancing Variables.pdf",height =6,width = 7.5 )




library(xtable)
print(xtable(basics),type="html",file="Total Activity Analysis_RaceAndGenderAndParty_v1/totalsandmeansbyracegenderandparty.doc")


names(basics)
basics2=basics[,c(14,2:10)]
colnames(basics2)=c("","All","COVID","COVID-Dangers","COVID-Social Distancing","COVID-Events","COVID-Partisan","COVID-Women","COVID-Race","Budget")
print(xtable(basics2),type="html",file="Total Activity Analysis_RaceAndGenderAndParty_v1/meansbyraceandgenderandparty.doc")



general=glm(general ~rpg +senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State, family = "quasipoisson", data = by_leg2)

covid=glm(covid ~rpg +senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State+general_rescaled, family = "quasipoisson", data = by_leg2)
summary(covid)

testing=glm(testing ~rpg +senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State+general_rescaled, family = "quasipoisson", data = by_leg2)

socialdistance=glm(sd ~rpg +senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State+general_rescaled, family = "quasipoisson", data = by_leg2)

events=glm(event ~rpg +senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State+general_rescaled, family = "quasipoisson", data = by_leg2)

partisan=glm(partisan ~rpg+senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State+general_rescaled, family = "quasipoisson", data = by_leg2)

gender=glm(gender ~rpg+senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State+general_rescaled, family = "quasipoisson", data = by_leg2)

race=glm(racial ~rpg+senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State+general_rescaled, family = "quasipoisson", data = by_leg2)

summary(race)
sd_all=glm( all_sd~rpg+senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State+general_rescaled, family = "quasipoisson", data = by_leg2)

sd_non_covid_only=glm( non_covid_sd~rpg+senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State+general_rescaled, family = "quasipoisson", data = by_leg2)

budget=glm( budget~rpg+senator+age_rescaled+leader_or_chair+X.voteTrump2016_resclaed+Last.Vote.Share+Bill.Sponsor.2019_rescaled+COVID.Rate.per.100.000_rescaled+perc_white+Population.Density..Per.sq.mile._rescaled+College_Educated_rescaled+median_income_rescaled+State+general_rescaled, family = "quasipoisson", data = by_leg2)

library(texreg)
htmlreg(list(general,covid,testing,socialdistance,events,partisan,gender,race,budget),single.row=TRUE,caption = "Count Model Using Totals and White Men as Reference", file = "Total Activity Analysis_RaceAndGenderAndParty_v1/CountModel_WhiteGOPmen_reference_racegenderparty.doc",
        stars = c(.01,.05,.1),
        custom.model.names = c("All","COVID","COVID-Dangers","COVID-Social Distancing","COVID-Events","COVID-Partisan","COVID-Women","COVID-Race","Budget"),
custom.coef.names = c("Constant","Democratic White Men","Republican White Women","Democratic White Women","Democratic MOC","Democratic WOC","Senator","Age","Party Leader","Trump 2016 Vote Share","Previous Vote Share","2019 Bill Sponsorship","Covid Rate per 100,000","% White","Population Density","% College Educated","Median Income","GA Legislator","NV Legislator","NY Legislator","TX Legislator", "Total Posts"))



#Marginal Effects
library(margins)
library(ggplot2)
library(ggpubr)
theme_set(theme_pubr())
res <-margins(general, variables="rpg", data = by_leg2)
res2 <-margins(covid, variables="rpg", data = by_leg2)
res3 <-margins(socialdistance, variables="rpg", data = by_leg2)
res4 <-margins(events, variables="rpg", data = by_leg2)
res5<-margins(partisan, variables="rpg", data = by_leg2)
res6<-margins(gender, variables="rpg", data = by_leg2)
res7<-margins(race, variables="rpg", data = by_leg2)
res8<-margins(sd_all, variables="rpg", data = by_leg2)
res9<-margins(sd_non_covid_only, variables="rpg", data = by_leg2)
res10<-margins(testing, variables="rpg", data = by_leg2)
res11<-margins(budget, variables="rpg", data = by_leg2)


gen_marg=as.data.frame(summary(res))
covid_marg=as.data.frame(summary(res2))
sd_marg=as.data.frame(summary(res3)) 
event_marg=as.data.frame(summary(res4))
partisan_marg=as.data.frame(summary(res5))
gender_marg=as.data.frame(summary(res6))
race_marg=as.data.frame(summary(res7))
sd_all_marg=as.data.frame(summary(res8))
non_covid_sd_marg=as.data.frame(summary(res9))
testing_marg=as.data.frame(summary(res10))
budget_marg=as.data.frame(summary(res11))

RGP=gsub("rpg", "", gen_marg$factor) #remove text from in front of group labels

gen_marg$RGP= RGP
sd_marg$RGP=RGP
covid_marg$RGP= RGP
event_marg$RGP=RGP
partisan_marg$RGP= RGP
gender_marg$RGP= RGP
race_marg$RGP= RGP
sd_all_marg$RGP= RGP
non_covid_sd_marg$RGP= RGP
testing_marg$RGP= RGP
budget_marg$RGP=RGP


gen_marg$RGP=factor(gen_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color"))
covid_marg$RGP=factor(covid_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color"))
sd_marg$RGP=factor(sd_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color"))                                    
event_marg$RGP=factor(event_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color"))
partisan_marg$RGP=factor(partisan_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color")) 
gender_marg$RGP=factor(gender_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color")) 
race_marg$RGP=factor(race_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color")) 
sd_all_marg$RGP=factor(sd_all_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color")) 
non_covid_sd_marg$RGP=factor(non_covid_sd_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color")) 
testing_marg$RGP=factor(testing_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color")) 
budget_marg$RGP=factor(budget_marg$RGP,levels = c("Republican White Women","Democratic White Men","Democratic White Women","Democratic Men of Color","Democratic Women of Color")) 
                                        

 
f1=ggplot(gen_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0, alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count") + ggtitle("All")+coord_flip()


f2=ggplot(covid_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0,  alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count")+ ggtitle("COVID")+coord_flip()
                 
f3=ggplot(sd_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0,  alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count")+ ggtitle("COVID-Social Distancing")+coord_flip()

f4=ggplot(event_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0,  alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count")+ ggtitle("COVID-Events")+coord_flip()

f5=ggplot(partisan_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0,  alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count")+ggtitle("COVID-Partisan")+coord_flip()


f6=ggplot(gender_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0,  alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count")+ggtitle("COVID-Women")+coord_flip()

f7=ggplot(race_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0,  alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count")+ggtitle("COVID-Race")+coord_flip()


f8=ggplot(sd_all_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0,  alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count")+ggtitle("All Social Distancing")+coord_flip()


f9=ggplot(non_covid_sd_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0,  alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count")+ggtitle("Non-COVID Social Distancing")+coord_flip()

f10=ggplot(testing_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0,  alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count")+ggtitle("COVID-Dangers")+coord_flip()

f11=ggplot(budget_marg,aes(x=RGP, y=AME))+
  geom_point(size=2)+
  geom_errorbar(aes(ymin=lower, ymax=upper), width=0, size=1.2)+
    geom_hline(yintercept=0,  alpha=.6)+
  theme_bw()+
  xlab("")+
  ylab("Difference in Expected Count")+ggtitle("Budget")+coord_flip()


together <- ggarrange(f2,f10,f3,f4,f5,f6,f7, ncol = 2, nrow = 4,common.legend = TRUE, legend = "none",font.label = list(size=12),vjust = .5)
ggexport(together,filename = "Total Activity Analysis_RaceAndGenderAndParty_v1/marginaleffects_white_men_gop.pdf",height =9,width = 8 )


gen_marg$AME=round(gen_marg$AME,2)
covid_marg$AME=round(covid_marg$AME,2)
sd_marg$AME=round(sd_marg$AME,2)
event_marg$AME=round(event_marg$AME,2)
partisan_marg$AME=round(partisan_marg$AME,2)
gender_marg$AME=round(gender_marg$AME,2)
race_marg$AME=round(race_marg$AME,2)
testing_marg$AME=round(testing_marg$AME,2)


gen_marg$CI <-paste(round(gen_marg$lower,2),round(gen_marg$upper,2))
covid_marg$CI <-paste(round(covid_marg$lower,2),round(covid_marg$upper,2))
sd_marg$CI <-paste(round(sd_marg$lower,2),round(sd_marg$upper,2))
event_marg$CI <-paste(round(event_marg$lower,2),round(event_marg$upper,2))
partisan_marg$CI <-paste(round(partisan_marg$lower,2),round(partisan_marg$upper,2))
gender_marg$CI <-paste(round(gender_marg$lower,2),round(gender_marg$upper,2))
race_marg$CI <-paste(round(race_marg$lower,2),round(race_marg$upper,2))
testing_marg$CI <-paste(round(testing_marg$lower,2),round(testing_marg$upper,2))



gen_marg$AME_CI=paste(gen_marg$AME, "(", gen_marg$CI, ")")
covid_marg$AME_CI=paste(covid_marg$AME, "(", covid_marg$CI, ")")
testing_marg$AME_CI=paste(testing_marg$AME, "(", testing_marg$CI, ")")
sd_marg$AME_CI=paste(sd_marg$AME, "(", sd_marg$CI, ")")
event_marg$AME_CI=paste(event_marg$AME, "(", event_marg$CI, ")")
partisan_marg$AME_CI=paste(partisan_marg$AME, "(", partisan_marg$CI, ")")
gender_marg$AME_CI=paste(gender_marg$AME, "(", gender_marg$CI, ")")
race_marg$AME_CI=paste(race_marg$AME, "(", race_marg$CI, ")")


names(testing_marg)

rg_me=cbind(covid_marg[,c(8,10)],testing_marg[,c(10)],sd_marg[,c(10)],event_marg[,c(10)],partisan_marg[,c(10)],gender_marg[,c(10)],race_marg[,c(10)]) #Table of Marginal Effects
colnames(rg_me)=c("Group","COVID","COVID-Dangers","COVID-Social Distancing", "COVID-Events","COVID-Partisan","COVID-Women","COVID-Race")

library(xtable)
print(xtable(rg_me),type="html",file="Total Activity Analysis_RaceAndGenderAndParty_v1/marginaleffects_table_white_men_gop.doc")
