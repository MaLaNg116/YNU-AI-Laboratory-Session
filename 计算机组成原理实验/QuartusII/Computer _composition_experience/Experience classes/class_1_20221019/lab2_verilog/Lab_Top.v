`default_nettype none 
//加减运算电路实验
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
wire M3   = SW[12];
wire M2   = SW[11];
wire M1   = SW[10];
wire M0   = SW[9];
wire Cin = SW[8];
wire [3:0] dst = SW[7:4];
wire [3:0] src = SW[3:0];

//各模块间连线信号
wire C0;
wire [3:0] B,F;
wire [3:0] FLAG;

//模块实例
ADDER #(.DATAWIDTH(4)) ADDER_inst(.A(dst), .B(B), .C0(C0), .F(F), .FLAG(FLAG)); 

assign B = {4{M1}} ^ (src & {4{M0}});
assign C0 = (Cin & M3) | (M2);

//内部信号赋值给输出端口（指示灯）观察
assign LEDR[3:0]  = B[3:0];
assign LEDR[7:4]  = dst[3:0]; 
assign LEDR[8] = Cin;
assign LEDR[16:13] = F;
assign LEDG[8] = C0; 
assign LEDG[3:0] = FLAG;

//内部信号赋值给输出端口（七段数码管）观察
assign HEX7 = 5'b11111; //消隐
assign HEX6 = dst;
assign HEX5 = 5'b11111; //消隐
assign HEX4 = B;
assign HEX3 = 5'b11111; //消隐
assign HEX2 = 5'b11111; //消隐
assign HEX1 = 5'b11111; //消隐
assign HEX0 = F;

endmodule
