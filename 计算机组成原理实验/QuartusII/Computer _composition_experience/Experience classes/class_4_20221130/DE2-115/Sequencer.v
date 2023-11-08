module Sequencer(
	input Clock,
	input Reset,     
	input Run,
	output reg CP1,
	output reg CP2
);

	always @(posedge Clock or posedge Reset) 
	begin 
		 if (Reset) 
		 begin 
			 CP1 <= 0;
			 CP2 <= 1;
			 end
		else
		begin
			CP1 <= CP2; 
			CP2 <= CP1;
		end
	end

endmodule 