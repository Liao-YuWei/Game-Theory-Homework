#include <iostream>
#include <iomanip>
#include <array>
#include <cstdlib>
#include <time.h>

class Player{
    private:
        unsigned int id;
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
            return;
        }
    
    public:
        Player(unsigned int player_id, std::array<std::array<int, 2>, 2> game, std::array<double, 2> init_belief) {
            id = player_id;
            std::copy(std::begin(game), std::end(game), std::begin(utility));
            std::copy(std::begin(init_belief), std::end(init_belief), std::begin(belief));
            calculate_payoff();
        }

        void update_belief(unsigned int strategy) {
            belief[strategy]++;
            calculate_payoff();
            return;
        }

        unsigned int respond() {
            if (payoff[0] > payoff[1])
                return 0;
            else if (payoff[1] > payoff[0])
                return 1;
            else
                return rand() % 2;
        }

        void print_belief_payoff() const {
            std::cout << "player" << id << "'s belief: " << belief[0] << "  "   << belief[1] << std::endl;
            std::cout << "player" << id << "'s payoff: " << payoff[0] << "  " << payoff[1] << std::endl << std::endl;
            return;
        } 
};

struct BestReponse {
    unsigned int p1;
    unsigned int p2;
};

float random_belief() {
    //return a flaot range in [0, 1000] 
    return (float)(rand() % 1000) + ((float)rand()/(float)(RAND_MAX));
}

void game_run(Player& player1, Player& player2) {
    BestReponse best_response;
    BestReponse pre_best_response;
    int iter = 1;
    int converge_count = 0;

    while(converge_count < 1000 && iter <= 6000) {
        std::cout << "Iteration: " << iter << std::endl;

        player1.print_belief_payoff();
        player2.print_belief_payoff();

        best_response.p1 = player1.respond();
        best_response.p2 = player2.respond();
        std::cout << "best response: " << best_response.p1 << ' ' << best_response.p2 << std::endl;

        player1.update_belief(best_response.p2);
        player2.update_belief(best_response.p1);

        if(pre_best_response.p1 == best_response.p1 && pre_best_response.p2 == best_response.p2)
            converge_count++;
        else
            converge_count = 0;
        pre_best_response.p1 = best_response.p1;
        pre_best_response.p2 = best_response.p2;
        iter++;

        std::cout << "--------------------------------" << std::endl;
    }

    return;
}

int main() {
    srand((unsigned) time(NULL));
    std::cout << std::setprecision(2) << std::fixed;

    unsigned int question;

    std::cout << "Please enter which question to solve(1~9): ";
    std::cin >> question;

    switch (question) {
        case 1: {   //Q1: One pure-strategy Nash Equilibrium
            Player player1(1, {{{-1, 1}, {0, 3}}}, {random_belief(), random_belief()});
            Player player2(2, {{{-1, 0}, {1, 3}}}, {random_belief(), random_belief()});
            game_run(player1, player2);
        }  
            break;

        case 2: {   //Q2: Two or more pure-strategy NE
            Player player1(1, {{{2, 1}, {0, 3}}}, {random_belief(), random_belief()});
            Player player2(2, {{{2, 0}, {1, 3}}}, {random_belief(), random_belief()});
            game_run(player1, player2);
        }
            break;
        
        case 3: {   //Q3: Two or more pure-strategy NE (Conti.)
            Player player1(1, {{{1, 0}, {0, 0}}}, {random_belief(), random_belief()});
            Player player2(2, {{{1, 0}, {0, 0}}}, {random_belief(), random_belief()});
            game_run(player1, player2);
        }
            break;
        
        case 4: {   //Q4: Mixed-Strategy Nash Equilibrium
            Player player1(1, {{{0, 2}, {2, 0}}}, {random_belief(), random_belief()});
            Player player2(2, {{{1, 0}, {0, 4}}}, {random_belief(), random_belief()});
            game_run(player1, player2);
        }
            break;

        case 5: {   //Q5: Best-reply path
            Player player1(1, {{{0, 1}, {1, 0}}}, {random_belief(), random_belief()});
            Player player2(2, {{{1, 0}, {0, 1}}}, {random_belief(), random_belief()});
            game_run(player1, player2);
        }
            break;

        case 6: {   //Q6: Pure-Coordination Game
            Player player1(1, {{{10, 0}, {0, 10}}}, {random_belief(), random_belief()});
            Player player2(2, {{{10, 0}, {0, 10}}}, {random_belief(), random_belief()});
            game_run(player1, player2);
        }
            break;

        case 7: {   //Q7: Anti-Coordination game
            Player player1(1, {{{0, 1}, {1, 0}}}, {random_belief(), random_belief()});
            Player player2(2, {{{0, 1}, {1, 0}}}, {random_belief(), random_belief()});
            game_run(player1, player2);
        }
            break;

        case 8: {   //Q8: Battle of the Sexes
            Player player1(1, {{{3, 0}, {0, 2}}}, {random_belief(), random_belief()});
            Player player2(2, {{{2, 0}, {0, 3}}}, {random_belief(), random_belief()});
            game_run(player1, player2);
        }
            break;
        
        case 9: {   //Q9: Stag Hunt Game
            Player player1(1, {{{3, 0}, {2, 1}}}, {random_belief(), random_belief()});
            Player player2(2, {{{3, 2}, {0, 1}}}, {random_belief(), random_belief()});
            game_run(player1, player2);
        }
            break;
        
        default:
            std::cout << "Wrong Input!!" << std::endl;
            break;
    }

    return 0;
}