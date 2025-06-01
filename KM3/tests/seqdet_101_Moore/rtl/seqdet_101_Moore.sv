`timescale 1ns / 1ps

module seqdet_101_Moore(
    input x, clk, rst,
    output y
    );
    reg y_reg;
    reg [1:0] currentstate, nextstate;
    parameter S0 = 2'b00;
    parameter S1 = 2'b01;
    parameter S2 = 2'b10;
    parameter S3 = 2'b11;


    always@(posedge clk or negedge rst)
    begin
        if(!rst)
            currentstate <= S0;
        else
            currentstate <= nextstate;
    end


    always@(currentstate or x or rst)
    begin
        if(!rst)
            nextstate = S0;
        else
        begin
            case(currentstate)
                S0:nextstate = (x==1) ? S1 : S0;
                S1:nextstate = (x==0) ? S2 : S0;
                S2:nextstate = (x==1) ? S3 : S0;
                S3:nextstate = (x==1) ? S1 : S0;
                default:nextstate = S0;
            endcase
        end
    end


    always@(rst or currentstate)
    begin
        if(!rst)
            y_reg = 0;
        else
        case(currentstate)
            S0:y_reg = 0;
            S1:y_reg = 0;
            S2:y_reg = 0;
            S3:y_reg = 1;
            default:y_reg = 0;
        endcase
    end

assign y = y_reg;

endmodule
