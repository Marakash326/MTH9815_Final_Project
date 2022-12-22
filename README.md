## Final_Project_Weiye_Jiang



- Before running the project, first delete all files in the `output` folder. You can also delete all files in the `input` folder, but that would mean you have to run `Generate_Data()` in the main function to generate the input files.

- The whole project might take 15-20 minutes to run,  depending on the platform and environment. Most of the time cost comes from processing `prices.txt` and `marketdata.txt` 

  

- The main function that tests the bond trading system consists of four parts:

  - Part (a).  Process trade booking data from `input/trades.txt`, and generate two output files: `output/positions.txt` and `output/risk.txt`. The data flow is

    - trades.txt -> trade booking service -> position service -> historical position service -> positions.txt
    - trades.txt -> trade booking service -> position service -> risk service -> historical risk service -> risk.txt
  - Part (b). Process price data from `input/prices.txt`, and generate two output files: `output/gui.txt` and `output/streaming.txt`. The data flow is

    - prices.txt -> pricing service -> gui service -> gui.txt
    - prices.txt -> pricing service -> also streaming service -> streaming service -> historical streaming service -> streaming.txt
  - Part (c). Process order book data from `input/marketorder.txt`, generate one file: `output/execution.txt` and update two files: `output/positions.txt` and `outpout/risk.txt`. The data flow is:

    - marketdata.txt -> market data service -> algo execution service -> execution service -> historical execution service -> executions.txt

    - marketdata.txt -> market data service -> algo execution service -> execution service -> trade booking service -> same as part (a)
  - Part (d). ​ Process inquiry data from `input/inquires.txt`, and generate one file: `output/all_inquiries.txt`. The data flow is:
    - inquiries.txt -> inquiry service -> historical inquiry service -> all_inquiries.txt



- About the input formats:
  - `trades.txt`: product ID, trade ID, book, price, quantity, side
  - `prices.txt`: product ID, bid price, offer price
  - `marketdata.txt`: product ID, bid price1, offer price1, bid price2, offer price2, bid price3, offer price3, bid price4, offer price4, bid price5, offer price5
  - `inquiries.txt`: product ID, inquiry ID, price, quantity, side, inquiry state



- About the output formats:
  - `positions.txt`: product ID, book1:quantity1 book2:quantity2 book3:quantity3
  - `risk.txt`: product ID, PV01 value, quantity
  - `gui.txt`: time stamp, product ID, mid price, bid offer spread
  - `streaming.txt`: product ID, bid price, offer price (The output in this file can be made more comprehensive easily but the time cost would be huge)
  - `executions.txt`: product ID, trade ID, side, price, visible quantity, hidden quantity
  - `all_inquiries.txt`: product ID, inquiry ID, side, price, inquiry state



