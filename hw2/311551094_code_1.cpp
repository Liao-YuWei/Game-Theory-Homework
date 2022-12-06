#include <iostream>
#include <array>

class Player{
    private:
        int id;
        std::array<std::array<int, 2>, 2> utility;
        std::array<double, 2> belief;
        std::array<double, 2> payoff;

        void calculate_payoff() {
            if (id == 1){
                payoff[0] = belief[0] * utility[0][0] + belief[1] * utility[0][1];
                payoff[1] = belief[0] * utility[1][0] + belief[1] * utility[1][1];
            }
            else if (id == 2){
                payoff[0] = belief[0] * utility[0][0] + belief[1] * utility[1][0];
                payoff[1] = belief[0] * utility[0][1] + belief[1] * utility[1][1];
            }
            // std::cout << payoff[0] << ' ' << payoff[1] << std::endl;
            return;
        }
    
    public:
        Player(int player_id, std::array<std::array<int, 2>, 2> game, std::array<double, 2> init_belief) {
            id = player_id;
            std::copy(std::begin(game), std::end(game), std::begin(utility));
            std::copy(std::begin(init_belief), std::end(init_belief), std::begin(belief));
            calculate_payoff();
        }

        int get_utility(int row, int col) const {
            return utility[row][col];
        } 

        int get_belief(int strategy) const {
            return belief[strategy];
        }

        void update_belief(int strategy) {
            belief[strategy]++;
            calculate_payoff();
            return;
        }
        
};

int main() {
    // std::array<std::array<int, 2>, 2> player1_utility = {{{-1, 1}, {0, 3}}};
    // std::array<std::array<int, 2>, 2> player2_utility = {{{-1, 0}, {1, 3}}};
    // std::array<int, 2> player1_belief = {0, 0};
    // std::array<int, 2> player2_belief = {0, 0};
    Player player1(1, {{{-1, 1}, {0, 3}}}, {1, 2});
    Player player2(2, {{{-1, 0}, {1, 3}}}, {4, 2});

    // std::cout << player1.get_utility(0, 1) << ' ' << player2.get_utility(0, 0) << std::endl;
    // std::cout << player1.get_belief(1) << ' ' << player2.get_belief(0) << std::endl;

    return 0;
}