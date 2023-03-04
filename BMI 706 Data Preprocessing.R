#####################################
# BMI 706, Data Visualization
# Data Pre-processing
# Author: Elombe Calvert
# March 3, 2023
#####################################

# Load Packages
library(tidyverse)
library(finalfit)
library(ggmap)
library(ggimage)

# Read in main data set
data <- read_csv("Mass PFAs Drinking Water.csv")

# Read in locations file
locations <- read_csv("massPWSLocations.csv")

# Merge and clean data files
merged_data <- left_join(data, locations, by=c("PWS ID"="PWS_ID")) %>% 
  select(c(`PWS ID`,Town,SITE_NAME,Class,`Chemical Name`,`Collected Date`,Result,
           LATITUDE,LONGITUDE)) %>% 
  filter(Result !="ND") %>% 
  drop_na(LATITUDE,LONGITUDE,Town,SITE_NAME) %>% 
  mutate(`Site ID` = `PWS ID`,Towns =Town,`Site` = SITE_NAME,Type=Class,
         Chemical=`Chemical Name`, Abbreviation= str_sub(Chemical,-5),
         Abbreviation= str_replace_all(Abbreviation, "-", ""),
         Abbreviation= str_replace_all(Abbreviation,c("FTRDA"="PFTRDA",
                                                      "F3ONS"="9CL-PF3ONS",
                                                      "3OUDS" ="11CL-PF3OUDS",
                                                      "PODA" ="HFPO-DA",
                                                      "FOSAA"="NMEFOSAA")),
         Date=`Collected Date`,Levels =as.numeric(Result),
         Latitude=LATITUDE,Longitude=LONGITUDE) %>% 
  .[,10:19]

# Save file
write_csv(merged_data,"Final Mass Data.csv")


Mass_box <- c(bottom = 41.24394, left  = -73.45850, 
                   top = 42.88459, right = -69.95256)

Mass <- get_stamenmap(Mass_box, 
                           maptype = "terrain", 
                           zoom = 5)
p_Mass <- Mass %>% 
  ggmap() +
  theme_void()

p_Mass + geom_point(data = merged_data, aes(Longitude, Latitude), 
                         color = "blue",na.rm = T)
