`default_nettype none 
//运算器数据通路实验
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
wire RESET = ~KEY[0];
wire CLK = KEY[1];
wire Ace  = SW[17];
wire GRSce= SW[16];
wire PSWce= SW[15];
wire [1:0] ST_OP = SW[14:13];
wire [3:0] ALU_OP = SW[12:9];
wire DATAoe = SW[8];
wire GRSoe = SW[7];
wire Soe   = SW[6];
wire [1:0] INDEX = SW[5:4];
wire [3:0] DATA = SW[3:0];

//内部总线信号定义
wire [3:0]BUS;

//各模块间连线信号
wire [3:0] A, F;
wire [3:0] FLAG, PSW;
wire [3:0] GRS_Q;
wire [3:0] S_Q;

//模块实例
ALU #(.DATAWIDTH(4)) ALU_inst(.dst( A), .src(BUS), .F(F), .FLAG( FLAG), .CF(PSW[0]), .ALU_OP(ALU_OP));

GRS #(.DATAWIDTH(4), .INDEXWIDTH(2)) GRS_inst(.D(BUS ), .Q (GRS_Q), .ce(GRSce), .CLK(CLK), .INDEX(INDEX));

R #(.DATAWIDTH(4)) A_inst(.Q(A), .D(BUS), .CLK(CLK), .ce(Ace), .RESET(RESET));

SHIFTER #(.DATAWIDTH(4)) SHIFTER_inst(.Q(S_Q), .D(F), .CLK(CLK), .ST_OP(ST_OP), .RESET(RESET));

R #(.DATAWIDTH(4)) PSW_inst(.Q(PSW), .D(FLAG), .CLK(CLK), .ce(PSWce ), .RESET(RESET));

//三态缓冲器逻辑描述
assign BUS = Soe    ? S_Q   : 4'bzzzz;
assign BUS = GRSoe  ? GRS_Q : 4'bzzzz;
assign BUS = DATAoe ? DATA  : 4'bzzzz;

//输入端口赋值给输出端口观察
//assign LEDR[17:0]  = SW[17:0];

//内部信号赋值给输出端口（指示灯）观察
assign LEDG[8] = CLK; 
assign LEDG[7:4] = PSW;
assign LEDG[3:0] = FLAG;

//内部信号赋值给输出端口（七段数码管）观察
assign HEX7 = 5'b11111; //消隐
assign HEX6 = 5'b11111; //消隐
assign HEX5 = A;
assign HEX4 = (Soe|GRSoe|DATAoe) ? BUS : 5'b11111; //仅为了显示
assign HEX3 = GRS_Q;
assign HEX2 = 5'b11111; //消隐
assign HEX1 = S_Q;
assign HEX0 = F;

endmodule
