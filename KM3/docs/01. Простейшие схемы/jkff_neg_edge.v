`timescale 1ns / 1ps
module jkff_neg_edge(
    input j,
    input k,
    input clk,
    output q,
    output qbar
    );
    reg q,qbar;
    always @(negedge clk)
        begin
        case({j,k})
        2'b00 : q <= q;
        2'b01 : q <= 0;
        2'b10 : q <= 1;
        2'b11 : q <= ~q;
        endcase
    qbar = ~q;
    end
     
endmodule
