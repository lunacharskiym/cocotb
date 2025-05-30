// Детектор последовательности 1101 по Мили с перекрытием
module seqdet_ol (
    clk,
    reset,
    i_data,
    o_det
);


input logic clk;
input logic reset;
input logic i_data;
output logic o_det;

typedef enum {s0, s1, s2, s3} state_type;


state_type state_reg, state_next;

always_ff @ (posedge clk) 
    begin
        if (reset)
            state_reg <= s0;
        else
            state_reg <= state_next;
    end

always_comb 
    begin
        case (state_reg)
            s0:
                begin
                    if(i_data)
                        state_next = s1;
                    else
                        state_next = s0;
                    o_det = 1'b0;
                end
            s1:
                begin
                    if(i_data)
                        state_next = s2;
                    else
                        state_next = s0;
                    o_det = 1'b0;
                end
            s2:
                begin
                    if(i_data)
                        state_next = s2;
                    else
                        state_next = s3;
                    o_det = 1'b0;
                end
            s3:
                begin
                    if(i_data)
                        begin
                            state_next = s1;
                            o_det = 1'b1;
                        end
                    else
                        begin
                            state_next = s0;
                            o_det = 1'b1;
                        end
                end
            default: state_next = s0;
        endcase
    end

endmodule
