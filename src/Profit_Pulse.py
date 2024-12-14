# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:57:01 2024

@author: Sharma_Ankit
"""

import random
import matplotlib.pyplot as plt
import numpy as np

class Team:
    def __init__(self, name, events):
        self.name = name
        self.initial_balance_sheet_composition = {
            'Assets': {'Loans': 0, 'Investments': 0, 'Cash and Equivalents': 0},
            'Liabilities': {'Deposits': 0, 'Borrowings': 0, 'Equity': 0}
        }
        self.balance_sheet_compositions = [self.initial_balance_sheet_composition.copy()]  # Store initial balance sheet
        self.score = 0.0
        self.net_interest_margin = 0.0
        self.loan_quality = 0.0
        self.interest_rate_risk_management = 0.0
        self.profitability = 0.0
        self.decision_variables = {}  # Initialize decision variables
        self.updated_liabilities = {}  # Store the latest liabilities information
        self.scores_after_events = [0] * len(events)  # Store scores after each event
        self.cumulative_score = 0
        self.cumulative_scores = [] 

    def validate_percentage_input(self, prompt):
        while True:
            try:
                percentage = float(input(prompt))
                if 0 <= percentage <= 100:
                    return percentage
                else:
                    print("Please enter a value between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    def decide_initial_balance_sheet(self):
        print(f"\n{self.name}'s Initial Balance Sheet Composition:")
        
        # Validate and set initial balance sheet composition for Assets
        assets_loans = self.validate_percentage_input("Enter Loans (0 to 100%): ")
        assets_investments = self.validate_percentage_input("Enter Investments (0 to 100%): ")
        assets_cash_equivalents = 100 - assets_investments - assets_loans

        # Validate and set initial balance sheet composition for Liabilities
        liabilities_deposits = self.validate_percentage_input("Enter Deposits (0 to 100%): ")
        liabilities_borrowings = self.validate_percentage_input("Enter Borrowings (0 to 100%): ")
        liabilities_equity = 100 - liabilities_deposits - liabilities_borrowings

        self.initial_balance_sheet_composition = {
            'Assets': {'Loans': assets_loans, 'Investments': assets_investments, 'Cash and Equivalents': assets_cash_equivalents},
            'Liabilities': {'Deposits': liabilities_deposits, 'Borrowings': liabilities_borrowings, 'Equity': liabilities_equity}
        }

    def update_balance_sheet(self):
        print(f"\n{self.name}'s Updated Balance Sheet Composition:")

        # Validate and set updated balance sheet composition for Assets
        updated_assets_loans = self.validate_percentage_input("Enter Loans (0 to 100%): ")
        updated_assets_investments = self.validate_percentage_input("Enter Investments (0 to 100%): ")
        updated_assets_cash_equivalents = 100 - updated_assets_investments - updated_assets_loans

        # Validate and set updated balance sheet composition for Liabilities
        updated_liabilities_deposits = self.validate_percentage_input("Enter Deposits (0 to 100%): ")
        updated_liabilities_borrowings = self.validate_percentage_input("Enter Borrowings (0 to 100%): ")

        self.updated_liabilities = {
            'Deposits': updated_liabilities_deposits,
            'Borrowings': updated_liabilities_borrowings,
            'Equity': 100 - updated_liabilities_deposits - updated_liabilities_borrowings
        }

        # Save the updated balance sheet composition
        self.balance_sheet_compositions.append({
            'Assets': {'Loans': updated_assets_loans, 'Investments': updated_assets_investments, 'Cash and Equivalents': updated_assets_cash_equivalents},
            'Liabilities': self.updated_liabilities
        })

        
        # Update the instance variable for future reference
        # self.updated_liabilities = updated_liabilities
    
    
    def calculate_decision_variables(self):
        if len(self.balance_sheet_compositions) == 2:  # Calculate using initial and latest updated balance sheet
            initial_assets = self.initial_balance_sheet_composition["Assets"]
            initial_liabilities = self.initial_balance_sheet_composition["Liabilities"]
            latest_assets = self.balance_sheet_compositions[-1]["Assets"]
            latest_liabilities = self.balance_sheet_compositions[-1]["Liabilities"]
    
            # Calculate decision variables based on initial and latest updated balance sheet
            delta_loans = latest_assets['Loans'] - initial_assets['Loans']
            delta_investments = latest_assets['Investments'] - initial_assets['Investments']
            delta_deposits = latest_liabilities['Deposits'] - initial_liabilities['Deposits']
            delta_borrowings = latest_liabilities['Borrowings'] - initial_liabilities['Borrowings']
            delta_cash = latest_assets['Cash and Equivalents'] - initial_assets['Cash and Equivalents']
            delta_ce = delta_cash  # Assuming Cash and Equivalents (C&E) is represented by delta_cash
    
            # Store the calculated decision variables in the team instance
            self.decision_variables = {
                'Delta Loans': delta_loans,
                'Delta Investments': delta_investments,
                'Delta Deposits': delta_deposits,
                'Delta Borrowing': delta_borrowings,
                'Delta Cash and Equivalents': delta_cash,
                'Delta CE': delta_ce  # Added delta_ce to decision variables
            }
    
    
    def calculate_score(self, event_idx):
        # Update calculations for decision variables based on balance sheet changes
        delta_loans = self.decision_variables['Delta Loans']
        delta_investments = self.decision_variables['Delta Investments']
        delta_deposits = self.decision_variables['Delta Deposits']
        delta_borrowings = self.decision_variables['Delta Borrowing']
        delta_ce = self.decision_variables['Delta CE']
    
        # Calculate metrics based on decision variable scores
        self.net_interest_margin = 10 * delta_loans - 5 * delta_ce - 8 * delta_investments + 3 * delta_deposits
        self.loan_quality = 10 * delta_investments - 15 * delta_loans
        self.interest_rate_risk_management = 8 * delta_borrowings - 5 * delta_deposits
    
        # Additional calculations for Profitability metrics based on balance sheet changes
        # Adjust net_interest_income and interest_expense based on changes in balance sheet components
        net_interest_income = delta_loans * self.net_interest_margin
        loan_losses = delta_loans * (1 - abs(self.loan_quality))
        interest_expense = delta_deposits * self.interest_rate_risk_management
    
        net_profit = net_interest_income - loan_losses - interest_expense
        # Access the latest equity directly from the balance sheet composition
        equity = self.balance_sheet_compositions[-1]["Liabilities"]["Equity"]
        # Adjust profitability formula based on changes in balance sheet components
        self.profitability = net_profit / equity
    
        # Scoring logic based on metrics
        score_metrics = [
            self.net_interest_margin,
            self.loan_quality,
            self.interest_rate_risk_management,
            self.profitability
        ]
    
        # Scale each metric to be in [-1, 0, 1]
        scaled_metrics = [1 if metric > 0 else (-1 if metric < 0 else 0) for metric in score_metrics]  
        
        # Calculate the score based on scaled metrics and weights
        self.score = (
            int(scaled_metrics[0] * 1.33) +  # Scale up to [-4, 4]
            int(scaled_metrics[1] * 1) +
            int(scaled_metrics[2] * 1) +
            int(scaled_metrics[3] * 0.67)  # Scale up to [-4, 4]
                    )
        
        # Apply bonus or penalty
        if all(metric > 0 for metric in scaled_metrics):
            self.score += 1  # +1 bonus point
        elif all(metric < 0 for metric in scaled_metrics):
            self.score -= 1  # -1 penalty point   

    
    def print_balance_sheet(self):
        print(f"{self.name}'s Updated Balance Sheet Composition:")
        print(f"  Assets:")
        for asset, value in self.balance_sheet_compositions[-1]["Assets"].items():
            print(f"    {asset}: {value:.2f}%")
        print(f"  Liabilities:")
        for liability, value in self.balance_sheet_compositions[-1]["Liabilities"].items():
            print(f"    {liability}: {value:.2f}%")
    
    
    def print_results(self):
        print(f"\nResults after the round:")
        print(f"{self.name}: Score = {self.score:.2f}")
        print(f"  Net Interest Margin: {self.net_interest_margin:.2f}")
        print(f"  Loan Quality: {self.loan_quality:.2f}")
        print(f"  Interest Rate Risk Management: {self.interest_rate_risk_management:.2f}")
        print(f"  Profitability: {self.profitability:.2f}")
        self.print_balance_sheet()
    
    
    def plot_event_scores(self, event_name, team_names, scores):
            plt.figure(figsize=(10, 6))
            plt.bar(team_names, scores, color=['blue', 'green'])  # Assuming two teams for illustration
            plt.title(f"Scores in {event_name}")
            plt.xlabel("Team")
            plt.ylabel("Score")
            plt.show()
            
    def plot_event_and_final_scores(self, event_names, scores_after_events, cumulative_scores, team_names):
        num_teams = len(team_names)
    
        # Plot scores after each event for each team
        plt.figure(figsize=(15, 6))
        for i, event_name in enumerate(event_names):
            plt.subplot(1, len(event_names), i + 1)
            for j in range(num_teams):
                plt.bar(j, scores_after_events[j][i], width=0.2, label=f"{team_names[j]}")
            plt.xlabel("Teams")
            plt.ylabel("Score")
            plt.title(f"Scores After {event_name}")
            plt.legend()
    
        plt.tight_layout()
        plt.show()
    
        # Plot cumulative scores for each team
        plt.figure(figsize=(10, 6))
        for j in range(num_teams):
            plt.bar(j, cumulative_scores[j][-1], width=0.2, label=f"{team_names[j]}")
    
        plt.xlabel("Teams")
        plt.ylabel("Cumulative Score")
        plt.title("Cumulative Scores After All Events")
        plt.legend()
        plt.show()



    def plot_cumulative_scores(self, team_names, cumulative_scores):
        plt.figure(figsize=(10, 6))
        
        for i, team_name in enumerate(team_names):
            plt.bar(i, cumulative_scores[-1][i], width=0.2, label=f"{team_name}")
    
        # Set labels and title
        plt.xlabel("Teams")
        plt.ylabel("Cumulative Score")
        plt.title("Cumulative Scores After Each Event")
    
        # Display legend
        plt.legend()
        plt.show()



def run_simulation(team_names, events):
    teams = [Team(name, events) for name in team_names]

    for event_idx, event in enumerate(events):
        print(f"\nEconomic Event: {event['name']}")
        for team_idx, team in enumerate(teams):
            if event == events[0]:  # Take initial balance sheet only before the first event
                team.decide_initial_balance_sheet()
                team.print_balance_sheet()
            else:
                print(f"\n{team.name}'s Updated Balance Sheet Composition (Before Update):")
                team.print_balance_sheet()
                # Update balance sheet
                team.update_balance_sheet()
                print(f"\n{team.name}'s Updated Balance Sheet Composition (After Update):")
                team.print_balance_sheet()
                # Calculate decision variables
                team.calculate_decision_variables()
                # Calculate and print the score
                team.calculate_score(event_idx)
                team.print_results()
                # Collect the score after the event
                team.scores_after_events[event_idx] = team.score

    # Calculate cumulative scores after each event
    for event_idx in range(len(events)):
        for team in teams:
            team.cumulative_score += team.scores_after_events[event_idx]
            team.cumulative_scores.append(team.cumulative_score)


    print("\nSimulation completed.")
    print("Final results:")
    for team in teams:
        print(f"{team.name}: Score = {team.cumulative_score:.2f}")

    # Plot scores after each event and final cumulative scores
    teams[0].plot_event_and_final_scores([event['name'] for event in events], [team.scores_after_events for team in teams], [team.cumulative_scores for team in teams], team_names)


# Example usage
if __name__ == "__main__":
    team_names = ["Team A", "Team B", "Team C", "Team D"]
    events = [
        {
            'name': "First Event",
        },
        {
            'name': "Second Event",
        },
        {
            'name': "Third Event",
        },        
        {
            'name': "Fourth Event",
        }
    ]
    run_simulation(team_names, events)