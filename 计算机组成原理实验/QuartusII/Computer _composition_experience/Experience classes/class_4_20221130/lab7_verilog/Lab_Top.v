`default_nettype none 
//微程序控制器实验
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
wire RESET = ~ KEY[0];
wire Clock = KEY[1];
wire [9:0] IR_D = SW[9:0];

//内部总线信号定义
wire [3:0]BUS;

//各模块间连线信号
wire [3:0] A, F;
wire [3:0] FLAG, PSW;
wire [3:0] GRS_Q;
wire [3:0] S_Q;
wire [9:0] IR_Q;

//模块实例
wire CP1, CP2;
wire [5:0] uAG_Out, uAR;
wire [19:0] CMdata, uIR;

//时序发生器
Sequencer Sequencer_inst(.Reset(RESET), .Clock(Clock), .CP1(CP1), .CP2(CP2));	

//微地址寄存器的副本，用于输出观察
R #(.DATAWIDTH(6)) uAR_inst
    (.Q(uAR), .D(uAG_Out), .CLK(CP1), .ce(1'b1), .RESET(RESET));

//控制存储器
`ifdef XILINX
  ControlMemory CM(.addra(uAG_Out), .clka(CP1), .douta(CMdata));
`else
  ControlMemory CM(.address(uAG_Out), .clock(CP1), .q(CMdata));
`endif

//微指令寄存器
R #(.DATAWIDTH(20)) uIR_inst
    (.Q(uIR), .D(CMdata), .CLK(CP2), .ce(1'b1), .RESET(RESET));

//微指令译码
wire GRSce, Ace, PSWce, IRce, NOP1; 
wire DATAoe, GRSoe, Soe, NOP2;
assign {DATAoe, Soe, GRSoe, NOP2} = 2**uIR[19:17];
assign {IRce, PSWce,Ace,GRSce,NOP1} = 2**uIR[16:14];
wire [3:0] ALU_OP = uIR[13:10];
wire [1:0] ST_OP = uIR[9:8];
wire [1:0] BM = uIR[7:6];
wire [4:0] NA = uIR[5:0];
    
//指令寄存器IR
R #(.DATAWIDTH(10)) IR_inst(.Q(IR_Q), .D(IR_D), .CLK(CP1), .ce(IRce), .RESET(RESET));
wire [1:0] INDEX = IR_Q[5:4];
wire [3:0] DATA = IR_Q[3:0];

//微地址形成
uAG uAG_inst(.uAGOut(uAG_Out), .IR(IR_Q[9:6]), .NA(NA), .BM(BM));

//运算器数据通路
wire CLK = CP1;
ALU #(.DATAWIDTH(4)) ALU_inst(.dst( A),.src(BUS),.F(F),.FLAG( FLAG),.CF(PSW[0]),.ALU_OP(ALU_OP));
GRS #(.DATAWIDTH(4),.INDEXWIDTH(2)) GRS_inst(.D(BUS ),.Q (GRS_Q),.ce(GRSce),.CLK(CLK),.INDEX(INDEX));
R #(.DATAWIDTH(4)) A_inst(.Q(A),.D(BUS),.CLK(CLK),.ce(Ace),.RESET(RESET));
SHIFTER #(.DATAWIDTH(4)) SHIFTER_inst(.Q (S_Q),.D (F),.CLK(CLK),.ST_OP(ST_OP),.RESET(RESET));
R #(.DATAWIDTH(4)) PSW_inst(.Q(PSW),.D(FLAG),.CLK(CLK),.ce(PSWce ),.RESET(RESET));
assign BUS = DATAoe ? DATA   : 4'bzzzz;
assign BUS = GRSoe  ? GRS_Q : 4'bzzzz;
assign BUS = Soe    ? S_Q   : 4'bzzzz;

//内部信号赋值给输出端口（指示灯）观察
assign LEDR[17]  = DATAoe;
assign LEDR[16]  = GRSoe;
assign LEDR[15]  = Soe;
assign LEDR[14]  = GRSce;
assign LEDR[13]  = Ace;
assign LEDR[12]  = PSWce;
assign LEDR[11:8]  = ALU_OP; 
assign LEDR[7:6]  = ST_OP; 
assign LEDR[5:4]  = uAR[5:4]; 
assign LEDR[3:0]  = uAR[3:0]; 
assign LEDG[8] = IRce; 
assign LEDG[7:4]  = PSW;
assign LEDG[3:2]  = INDEX;
assign LEDG[1] = CP1; 
assign LEDG[0] = CP2; 

//内部信号赋值给输出端口（七段数码管）观察
assign HEX7 = A;
assign HEX6 = BUS;
assign HEX5 = S_Q;
assign HEX4 = CMdata[19:16];
assign HEX3 = CMdata[15:12];
assign HEX2 = CMdata[11:8];
assign HEX1 = CMdata[7:4];
assign HEX0 = CMdata[3:0];  
endmodule
