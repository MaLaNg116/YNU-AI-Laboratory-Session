`default_nettype none
module DE2_115_TOP(
    //////////// CLOCK //////////
    input               CLOCK_50,
    input               CLOCK2_50,
    input               CLOCK3_50,
    input               ENETCLK_25,
    
    //////////// Sma //////////
    input               SMA_CLKIN,
    output              SMA_CLKOUT,
    
    //////////// LED //////////
    output       [8:0]  LEDG,
    output      [17:0]  LEDR,
    
    //////////// KEY //////////
    input        [3:0]  KEY,
    
    //////////// SW //////////
    input       [17:0]  SW,
    
    //////////// SEG7 //////////
    output       [6:0]  HEX0,
    output       [6:0]  HEX1,
    output       [6:0]  HEX2,
    output       [6:0]  HEX3,
    output       [6:0]  HEX4,
    output       [6:0]  HEX5,
    output       [6:0]  HEX6,
    output       [6:0]  HEX7,
    
    //////////// LCD //////////
    output              LCD_BLON,
    inout        [7:0]  LCD_DATA,
    output              LCD_EN,
    output              LCD_ON,
    output              LCD_RS,
    output              LCD_RW,
    
    //////////// RS232 //////////
    output              UART_CTS,
    input               UART_RTS,
    input               UART_RXD,
    output              UART_TXD,
    
    //////////// PS2 //////////
    inout               PS2_CLK,
    inout               PS2_DAT,
    inout               PS2_CLK2,
    inout               PS2_DAT2,
    
    //////////// SDCARD //////////
    output              SD_CLK,
    inout               SD_CMD,
    inout        [3:0]  SD_DAT,
    input               SD_WP_N,
    
    //////////// VGA //////////
    output       [7:0]  VGA_B,
    output              VGA_BLANK_N,
    output              VGA_CLK,
    output       [7:0]  VGA_G,
    output              VGA_HS,
    output       [7:0]  VGA_R,
    output              VGA_SYNC_N,
    output              VGA_VS,
    
    //////////// Audio //////////
    input               AUD_ADCDAT,
    inout               AUD_ADCLRCK,
    inout               AUD_BCLK,
    output              AUD_DACDAT,
    inout               AUD_DACLRCK,
    output              AUD_XCK,
    
    //////////// I2C for EEPROM //////////
    output              EEP_I2C_SCLK,
    inout               EEP_I2C_SDAT,
    
    //////////// I2C for Audio and Tv-Decode //////////
    output              I2C_SCLK,
    inout               I2C_SDAT,
    
    //////////// Ethernet 0 //////////
    output              ENET0_GTX_CLK,
    input               ENET0_INT_N,
    output              ENET0_MDC,
    inout               ENET0_MDIO,
    output              ENET0_RST_N,
    input               ENET0_RX_CLK,
    input               ENET0_RX_COL,
    input               ENET0_RX_CRS,
    input        [3:0]  ENET0_RX_DATA,
    input               ENET0_RX_DV,
    input               ENET0_RX_ER,
    input               ENET0_TX_CLK,
    output       [3:0]  ENET0_TX_DATA,
    output              ENET0_TX_EN,
    output              ENET0_TX_ER,
    input               ENET0_LINK100,
    
    //////////// Ethernet 1 //////////
    output              ENET1_GTX_CLK,
    input               ENET1_INT_N,
    output              ENET1_MDC,
    inout               ENET1_MDIO,
    output              ENET1_RST_N,
    input               ENET1_RX_CLK,
    input               ENET1_RX_COL,
    input               ENET1_RX_CRS,
    input        [3:0]  ENET1_RX_DATA,
    input               ENET1_RX_DV,
    input               ENET1_RX_ER,
    input               ENET1_TX_CLK,
    output       [3:0]  ENET1_TX_DATA,
    output              ENET1_TX_EN,
    output              ENET1_TX_ER,
    input               ENET1_LINK100,
    
    //////////// TV Decoder 1 //////////
    input               TD_CLK27,
    input        [7:0]  TD_DATA,
    input               TD_HS,
    output              TD_RESET_N,
    input               TD_VS,
    
    
    //////////// USB OTG controller //////////
    inout       [15:0]  OTG_DATA,
    output       [1:0]  OTG_ADDR,
    output              OTG_CS_N,
    output              OTG_WR_N,
    output              OTG_RD_N,
    input        [1:0]  OTG_INT,
    output              OTG_RST_N,
    input        [1:0]  OTG_DREQ,
    output       [1:0]  OTG_DACK_N,
    inout               OTG_FSPEED,
    inout               OTG_LSPEED,
    
    //////////// IR Receiver //////////
    input               IRDA_RXD,
    
    //////////// SDRAM //////////
    output      [12:0]  DRAM_ADDR,
    output       [1:0]  DRAM_BA,
    output              DRAM_CAS_N,
    output              DRAM_CKE,
    output              DRAM_CLK,
    output              DRAM_CS_N,
    inout       [31:0]  DRAM_DQ,
    output       [3:0]  DRAM_DQM,
    output              DRAM_RAS_N,
    output              DRAM_WE_N,
    
    //////////// SRAM //////////
    output      [19:0]  SRAM_ADDR,
    output              SRAM_CE_N,
    inout       [15:0]  SRAM_DQ,
    output              SRAM_LB_N,
    output              SRAM_OE_N,
    output              SRAM_UB_N,
    output              SRAM_WE_N,
    
    //////////// Flash //////////
    output      [22:0]  FL_ADDR,
    output              FL_CE_N,
    inout        [7:0]  FL_DQ,
    output              FL_OE_N,
    output              FL_RST_N,
    input               FL_RY,
    output              FL_WE_N,
    output              FL_WP_N,
    
    //////////// GPIO //////////
    inout       [35:0]  GPIO,
    
    //////////// HSMC (LVDS) //////////
    
    //input              HSMC_CLKIN_N1;
    //input              HSMC_CLKIN_N2;
    input               HSMC_CLKIN_P1,
    input               HSMC_CLKIN_P2,
    input               HSMC_CLKIN0,
    //output              HSMC_CLKOUT_N1;
    //output              HSMC_CLKOUT_N2;
    output              HSMC_CLKOUT_P1,
    output              HSMC_CLKOUT_P2,
    output              HSMC_CLKOUT0,
    inout        [3:0]  HSMC_D,
    //input      [16:0]  HSMC_RX_D_N;
    input       [16:0]  HSMC_RX_D_P,
    //output      [16:0]  HSMC_TX_D_N;
    output      [16:0]  HSMC_TX_D_P,
    
    ///////// DEBUG IO ///////////
    output              JRXD,
    input               JTXD,
    input               JTRST_n,
    input               JTCK,
    input               TMS,
    input               TDI,
    output              TDO
);

    //  All inout port turn to tri-state
    assign  DRAM_DQ     =   16'hzzzz;
    assign  FL_DQ           =   8'hzz;
    assign  SRAM_DQ     =   16'hzzzz;
    assign  SD_DAT      =   1'bz;
    assign  I2C_SDAT        =   1'bz;
    assign  AUD_ADCLRCK =   1'bz;
    assign  AUD_DACLRCK =   1'bz;
    assign  AUD_BCLK        =   1'bz;
    assign  GPIO            =   36'hzzzzzzzzz;
  assign  JRXD = JTXD;
    
//---------------------------------------------------------------------------// 
    wire [3:0] mKEY_BSC;
    wire [17:0]mSW_BSC;
    wire [4:0] mHex [0:7];

    Lab_Top Lab_inst(
        .CLOCK(CLOCK_50),
        .KEY(mKEY_BSC),
        .SW(mSW_BSC),
        .LEDR(LEDR),
        .LEDG(LEDG),
        .HEX7(mHex[7]),
        .HEX6(mHex[6]),
        .HEX5(mHex[5]),
        .HEX4(mHex[4]),
        .HEX3(mHex[3]),
        .HEX2(mHex[2]),
        .HEX1(mHex[1]),
        .HEX0(mHex[0])
    );

    // 七段数码管译码
    SEG7_LUT u7(.oSEG(HEX7),.iDIG(mHex[7]));
    SEG7_LUT u6(.oSEG(HEX6),.iDIG(mHex[6]));
    SEG7_LUT u5(.oSEG(HEX5),.iDIG(mHex[5]));
    SEG7_LUT u4(.oSEG(HEX4),.iDIG(mHex[4]));
    SEG7_LUT u3(.oSEG(HEX3),.iDIG(mHex[3]));
    SEG7_LUT u2(.oSEG(HEX2),.iDIG(mHex[2]));
    SEG7_LUT u1(.oSEG(HEX1),.iDIG(mHex[1]));
    SEG7_LUT u0(.oSEG(HEX0),.iDIG(mHex[0]));
    
//---------------------------------------------------------------------------//
    wire TCK;
    GlobalCLK globalTCK_inst(
        .ena(1'b1),
        .inclk (JTCK),
        .outclk (TCK)
    );
    
    wire [10:0] mBSR_Select;
    wire [10:0] mBSR_ScanOut;
    wire mShiftDR, mCaptureDR, mUpdateDR,mMode;
    wire mJTAG_Reset;
    JtagForDebug  jtagForDebug_inst
    (
        .iTCK (TCK),
        .iTMS (TMS),
        .iTDI (TDI),
        .oTDO (TDO),
        .iBSR_ScanOut (mBSR_ScanOut),
        .oBSR_Select (mBSR_Select),
        .oShiftDR (mShiftDR),
        .oCaptureDR (mCaptureDR),
        .oUpdateDR (mUpdateDR),
        .oMode(mMode),
        .oJTAG_Reset (mJTAG_Reset)
    );

//---------------------------------------------------------------------------// 
    wire mSelect_HEX= mBSR_Select[10]; 
    wire mSelect_KEY = mBSR_Select[9];
    wire mSelect_LED = mBSR_Select[8];
    wire mSelect_SW = mBSR_Select[7];
    
    wire mHEX_ScanOut,mKEY_ScanOut,mLED_ScanOut, mSW_ScanOut;
    assign mBSR_ScanOut[10] = mHEX_ScanOut;
    assign mBSR_ScanOut[9] = mKEY_ScanOut;
    assign mBSR_ScanOut[8] = mLED_ScanOut;
    assign mBSR_ScanOut[7] = mSW_ScanOut;

    //SW 拨动开关扫描链    
    BSC #(.DATAWIDTH(18)) bsc_SW(
        .DataIn(SW), .DataOut(mSW_BSC),
        .ScanIn(TDI), .ScanOut(mSW_ScanOut), 
        .ShiftDR(mSelect_SW & mShiftDR), 
        .CaptureDR(mSelect_SW & mCaptureDR), 
        .UpdateDR(mSelect_SW & mUpdateDR),
        .TCK(TCK), .Mode(mMode)
    );  

    //KEY 按键扫描链
    BSC #(.DATAWIDTH(4)) bsc_KEY(
        .DataIn(KEY), .DataOut(mKEY_BSC),
        .ScanIn(TDI), .ScanOut(mKEY_ScanOut), 
        .ShiftDR(mSelect_KEY & mShiftDR), 
        .CaptureDR(mSelect_KEY & mCaptureDR), 
        .UpdateDR(mSelect_KEY & mUpdateDR), 
        .Mode(mMode), .TCK(TCK)
    );
    
    //LED 指示灯扫描链    
    BSC #(.DATAWIDTH(27)) bsc_LED(
        .DataIn({LEDR,LEDG}), .DataOut(),
        .ScanIn(TDI), .ScanOut(mLED_ScanOut), 
        .ShiftDR(mSelect_LED & mShiftDR), 
        .CaptureDR(mSelect_LED & mCaptureDR), 
        .UpdateDR(mSelect_LED & mUpdateDR),
        .TCK(TCK), .Mode(0)
    );  
    
    //HEX 数码管扫描链
    BSC #(.DATAWIDTH(56)) bsc_HEX(
        .DataIn({HEX7,HEX6,HEX5,HEX4,HEX3,HEX2,HEX1,HEX0}), 
        .DataOut(),
        .ScanIn(TDI), .ScanOut(mHEX_ScanOut), 
        .ShiftDR(mSelect_HEX & mShiftDR), 
        .CaptureDR(mSelect_HEX & mCaptureDR), 
        .UpdateDR(mSelect_HEX & mUpdateDR),
        .TCK(TCK), .Mode(0)
    );

endmodule