library(tidyverse)
path='c:/resolve/projects/magento'
setwd(path)

order_details <- data.frame(read_csv('magento orders 2-1-2017.csv'))
orders <- data.frame(read_csv('magento 2-1-2017.csv', n_max = 10))

city_group <- data.frame(order_details %>%
  filter(address_type == 'billing') %>%
  group_by(city, name) %>%
  summarise(
    num_sold = sum(qty_ordered)    ))

product_group <- data.frame(order_details %>%
   filter(address_type == 'billing') %>%
   group_by(name, sku, price) %>%
   summarise(
     var = var(base_row_total)    ))

'product
category
cohort'

ytd <- data.frame(read.csv('c:/tony/downloads/lbr.csv') %>%
                    group_by(Department, Process.Number) %>%
                    filter(!grepl('MGT', Department)) %>%
                    filter(grepl('OT', DET.Code)) %>%
                    summarise(ytdpay = sum(Earning.Amount)) )
