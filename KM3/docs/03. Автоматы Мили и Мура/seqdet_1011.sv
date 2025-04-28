`timescale 1ns/1ns

// Поиск последовательности 1011
 module seqdet_1011
 (
    input  clk,
    input  rst_n,
    input  din,
    output check_vld
 );


 parameter IDLE = 5'b00001;
 parameter S1   = 5'b00010;
 parameter S2   = 5'b00100;
 parameter S3   = 5'b01000;
 parameter S4   = 5'b10000;


reg [4:0] c_state;
reg [4:0] n_state;
reg       check_vld;


always @(posedge clk or negedge rst_n)
begin
    if (rst_n == 1'b0)
        c_state <= IDLE;
    else
        c_state <= n_state;
end


always @(*)
begin
   if(rst_n == 1'b0)
      n_state <= IDLE;
   else
   begin
      case(c_state)
        IDLE:
        begin
            if(din==1'b1)
                n_state <= S1;
            else
                n_state <= IDLE;
        end
        S1:
        begin
            if(din==1'b0)
               n_state <= S2;
            else
               n_state <= S1;
        end
        S2:
        begin
            if(din==1'b1)
               n_state <= S3;
            else
                n_state <= IDLE;
        end
        S3:
        begin
            if(din==1'b1)
               n_state <= S4;
            else
               n_state <= S2;
        end
        S4:
        begin
            if(din==1'b1)
               n_state <= S1;
            else
               n_state <= S2;
        end
        default:
            n_state <= IDLE;
    endcase
   end
end


always @(posedge clk or negedge rst_n)
begin
    if (rst_n == 1'b0)
        check_vld <= 1'b0;
    else if(n_state==S4)
        check_vld <= 1'b1;
    else
        check_vld <= 1'b0;
end
endmodule
