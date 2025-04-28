`timescale 1ns / 1ps

// Поиск последовательности 101 с перекрытием
module seqdet_101(
    input clk, rst, x,
    output y
    );


    reg y;
    reg temp_y;
    reg[1:0] currentstate, nextstate;


    parameter S0 = 2'b00;
    parameter S1 = 2'b01;
    parameter S2 = 2'b10;


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
            nextstate <= S0;
        else
            begin
                case(currentstate)
                    S0: nextstate = (x==1)?S1:S0;
                    S1: nextstate = (x==0)?S2:S0;
                    S2: nextstate = (x==1)?S1:S0;
                    default: nextstate = S0;
                endcase
            end
    end


    always@(rst or currentstate or x)
    begin
        if(!rst)
            temp_y = 0;
        else
            case(currentstate)
                S0: temp_y = 0;
                S1: temp_y = 0;
                S2: temp_y = (x==1)?1:0;
                default: temp_y = 0;
            endcase
    end


    always@(posedge clk or negedge rst)
    begin
        if(!rst)
            y <= 0;
        else
            begin
                //
                if((temp_y == 1)&&(nextstate == S1))
                    y <= 1;
                else
                    y <= 0;
            end
    end
endmodule
