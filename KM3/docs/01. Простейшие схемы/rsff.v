module rsff(sr,clk,q,qbar);
	input [1:0] sr;
	input clk;
	output q,qbar;
	reg q,qbar;

	always@(posedge clk)
	begin
	case(sr)
		2'b00:
			q = q;


		2'b01:
			q=0;

		2'b10:
			q=1;
	
		2'b11:
			q= 1'bz;
	endcase
	qbar = ~q;
	end 
endmodule
