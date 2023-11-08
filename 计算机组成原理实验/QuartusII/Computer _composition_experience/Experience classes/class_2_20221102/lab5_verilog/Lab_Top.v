`default_nettype none 
//高速缓存实验
module Lab_Top (
    // 端口定义
    input  wire  CLOCK,
    input  wire [17:0] SW,   //开关
    input  wire  [3:0] KEY,  //按键
    output wire [17:0] LEDR, //红色指示灯 
    output wire  [8:0] LEDG, //绿色指示灯
    output wire  [4:0] HEX7, //七段数码管
    output wire  [4:0] HEX6, //七段数码管
    output wire  [4:0] HEX5, //七段数码管
    output wire  [4:0] HEX4, //七段数码管
    output wire  [4:0] HEX3, //七段数码管
    output wire  [4:0] HEX2, //七段数码管
    output wire  [4:0] HEX1, //七段数码管
    output wire  [4:0] HEX0  //七段数码管
);

//输入端口赋值给内部信号
wire RESET         = ~KEY[0];
wire CLK           = KEY[1];
wire WR_CACHE      = ~KEY[2];
wire [1:0] OFFSET  = SW[5:4];
wire [7:0] AB      = SW[17:10];

//地址寄存器模块实例
wire [7:0] AR;
R #(8) AR_inst(.D(AB), .Q(AR), .CLK(CLK), .ce(1'b1), .RESET(RESET));
wire [2:0] field_TAG = AR[7:5];
wire [2:0] field_BLOCK = AR[4:2];
wire [1:0] field_WORD = AR[1:0];		  

//实例化主存储器
wire [3:0] MM_DATA;
ram_mm	ram_mm_inst (.address({field_TAG, field_BLOCK, OFFSET}), .clock(WR_CACHE), .data(), .wren(1'b0), .q(MM_DATA));

//译码产生CACHE的字写入信号
wire WR0, WR1, WR2, WR3;
Decode Decode_inst (.Enable(WR_CACHE), .DIN(OFFSET), .DOUT({WR3,WR2,WR1,WR0}));		
							  
//实例化TAG存储器
wire [2:0] TAG;
wire WR_TAG   = WR3;
ram_tag  TAG_inst(.q(TAG), .data(field_TAG), .address(field_BLOCK), .wren(1'b1), .clock(WR_TAG)); 


//VALID存储器
wire VALID;
wire [7:0] V_LED;
wire WR_VALID = WR3; 
ram_valid  VALID_inst(.VALID(VALID), .ADDR(field_BLOCK), .RESET(RESET), .WR(WR_VALID), .V_LED(V_LED)); 

//实例化CACHE存储器
wire [3:0] CACHE_WORD0,CACHE_WORD1,CACHE_WORD2,CACHE_WORD3;
ram_cache  DATA0 (.q(CACHE_WORD0), .data(MM_DATA), .address(field_BLOCK), .wren(1'b1), .clock(~WR0));
ram_cache  DATA1 (.q(CACHE_WORD1), .data(MM_DATA), .address(field_BLOCK), .wren(1'b1), .clock(~WR1));
ram_cache  DATA2 (.q(CACHE_WORD2), .data(MM_DATA), .address(field_BLOCK), .wren(1'b1), .clock(~WR2));
ram_cache  DATA3 (.q(CACHE_WORD3), .data(MM_DATA), .address(field_BLOCK), .wren(1'b1), .clock(~WR3));

//实例化多路选择器模块
wire [3:0] CACHE_WORD;
MUX  #(4) MUX_inst (.SEL(field_WORD), .A(CACHE_WORD0), .B(CACHE_WORD1), .C(CACHE_WORD2), .D(CACHE_WORD3), .MUX_OUT(CACHE_WORD));

//比较TAG存储器中读出的内容与当前地址寄存器AR中TAG字段的值是否相同，判断命中（HIT）
wire HIT;
assign  HIT = VALID ? (field_TAG == TAG) : 0 ;

//内部信号赋值给输出端口（指示灯）观察
assign LEDR[17:10] = AR[7:0]; 
assign LEDR[9] = WR_VALID;
assign LEDR[8] = WR_TAG;
assign LEDR[7] = WR3; 
assign LEDR[6] = WR2;
assign LEDR[5] = WR1;
assign LEDR[4] = WR0;
assign LEDR[3] = VALID;
assign LEDR[2:0] = TAG;
assign LEDG[8] = HIT;
assign LEDG[7:0] =  V_LED[7:0];

//内部信号赋值给输出端口（七段数码管）观察
assign HEX7 = 5'b11111; //消隐
assign HEX6 = CACHE_WORD[3:0]; 
assign HEX5 = 5'b11111; //消隐
assign HEX4 = MM_DATA[3:0]; 
assign HEX3 = CACHE_WORD3;
assign HEX2 = CACHE_WORD2;
assign HEX1 = CACHE_WORD1;
assign HEX0 = CACHE_WORD0;

endmodule
