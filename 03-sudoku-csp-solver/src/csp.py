from cnf import CNF


class CSP:
    def __init__(self, cnf: CNF, use_mcv=True, use_mrv=True, use_lcv=True):
        """
        Initializes a Constraint Satisfaction Problem (CSP) solver.

        Args:
            cnf (CNF): The Conjunctive Normal Form representation of the problem.
            use_mcv (bool): Whether to use Most Constraining Variable (MCV) or not. Defaults to True.
            use_mrv (bool): Whether to use Minimum Remaining Value (MRV) or not. Defaults to True.
            use_lcv (bool): Whether to use Least Constraining Value (LCV) or not. Defaults to True.
        """
        self.cnf = cnf
        self.use_mcv = use_mcv
        self.use_mrv = use_mrv
        self.use_lcv = use_lcv
        self.degree = {}
        self.variables = {}
        self.assigned_variables = {}
        self.constraints = []
        self.var_constraints = {}

        self.best_solution = None
        self.best_weight = float('-inf')

        # Used for pruning
        self.max_weight = sum(
            int(clause[-1]) for clause in cnf.soft_clauses if clause[-1].isdigit())

        for variable in cnf.variables:
            self.add_variable(variable, [False, True])
            self.degree[variable] = 0

        # Considering hard clausess
        for clause in cnf.hard_clauses:
            self.add_constraint(cnf.evaluate_clause, clause)
            # Updating the degree of variables
            for variable in clause:
                self.degree[variable] += 1

    def add_variable(self, variable, domain):
        """
        Adds a new variable with its given domain to the CSP solver.

        Args:
            variable (str): The name of the variable.
            domain ([bool]): The domain of the variable (in this case, [False, True]).
        """

        self.variables[variable] = domain

    def add_constraint(self, constraint_function, variables):
        """
        Adds a new constraint to the CSP solver.

        Args:
            constraint_function (function): A function that takes two arguments (a clause and assigned values) and returns True if the constraint is satisfied, False otherwise.
            variables ([str]): The list of variables involved in the constraint.
        """

        self.constraints.append((constraint_function, variables))
        for var in variables:
            if var not in self.var_constraints:
                self.var_constraints[var] = []
            self.var_constraints[var].append((constraint_function, variables))

    def assign(self, variable, value):
        """
         Assigns a specific value to a variable.

         Args:
             variable (str): The name of the variable.
             value (bool): The assigned value for the variable.
         """

        self.assigned_variables[variable] = value
        negation = variable[1:] if variable.startswith('~') else f'~{variable}'
        self.assigned_variables[negation] = not value

    def unassign(self, variable):
        """
        Unassigns a previously assigned value from a variable.

        Args:
            variable (str): The name of the variable.
        """

        if variable in self.assigned_variables:
            del self.assigned_variables[variable]
        negation = variable[1:] if variable.startswith('~') else f'~{variable}'
        del self.assigned_variables[negation]

    def is_constraint_satisfied(self, constraint):
        """
        Checks if a specific constraint is satisfied given the current assignment of variables.

        Args:
            constraint: A tuple containing the constraint function and the list of involved variables.

        Returns:
            bool: True if the constraint is satisfied, False otherwise.
        """

        constraint_function, variables = constraint
        assigned_values = {var: self.assigned_variables.get(
            var) for var in variables}
        return constraint_function(variables, assigned_values)

    def is_consistent(self, variable, value):
        """
        Checks if assigning a specific value to a variable would violate any constraints.

        Args:
            variable (str): The name of the variable.
            value (bool): The assigned value for the variable.

        Returns:
            bool: True if the assignment does not violate any constraints, False otherwise.
        """

        self.assign(variable, value)

        for constraint_function, variables in self.var_constraints.get(variable, []):
            # Checking hard constraints
            if not self.is_constraint_satisfied((constraint_function, variables)):
                self.unassign(variable)
                return False

        negation = variable[1:] if variable.startswith('~') else f'~{variable}'
        if negation in self.assigned_variables:
            for constraint_function, variables in self.var_constraints.get(negation, []):
                # Checking negated constraints
                if not self.is_constraint_satisfied((constraint_function, variables)):
                    self.unassign(variable)
                    return False

        self.unassign(variable)
        return True

    def is_complete(self):
        """
        Checks if all variables have been assigned a value.

        Returns:
            bool: True if the assignment is complete, False otherwise.
        """

        for variable in self.variables:
            if variable not in self.assigned_variables:
                return False
            if self.assigned_variables[variable] is None:
                return False
        return True

    def select_unassigned_variable(self):
        """
        Selects an unassigned variable to assign a value to next.

        Returns:
            str: The name of the selected variable.
        """

        unassigned_variables = [
            var for var in self.variables if var not in self.assigned_variables]
        if self.use_mrv:
            return self.minimum_remaining_value()
        elif self.use_mcv:
            return self.most_constraining_variable(unassigned_variables)
        return unassigned_variables[0]

    def solve(self):
        """
        Solves the CSP problem using backtracking search with MCV/LCV.

        Returns:
            tuple: A tuple containing the solution (a dictionary mapping variables to their assigned values)
                   and the best weight (the minimum weight of all possible solutions).
        """

        if self.is_complete():
            if self.cnf.are_all_satisfied(self.assigned_variables):
                return self.assigned_variables, self.cnf.calculate_weight(self.assigned_variables)
            return None, 0

        variable = self.select_unassigned_variable()
        domain = self.variables[variable]
        if self.use_lcv:
            domain = self.least_constraining_value(variable)

        for value in domain:
            if self.is_consistent(variable, value):
                self.assign(variable, value)
                result, weight = self.solve()
                if result is not None:
                    if weight > self.best_weight:
                        self.best_weight = weight
                        self.best_solution = result.copy()
                    # Pruning if possible
                    if self.best_weight == self.max_weight:
                        return self.best_solution, self.best_weight
                self.unassign(variable)

        return self.best_solution, self.best_weight

    def minimum_remaining_value(self):
        """ Selects the variable that appears in the fewest unsatisfied clauses. """

        unassigned_variables = [
            var for var in self.variables if var not in self.assigned_variables]

        def legal_values(var):
            count = 0
            for value in self.variables[var]:
                if self.is_consistent(var, value):
                    count += 1
            return count

        return min(unassigned_variables, key=legal_values)

    def most_constraining_variable(self, unassigned_variables):
        """
        Returns the variable that would violate the most constraints when assigned a value.

        Args:
            variables ([str]): The list of variables to consider.

        Returns:
            str: The name of the most constraining variable.
        """

        return max(unassigned_variables, key=lambda var: len(self.var_constraints.get(var, [])))

    def least_constraining_value(self, var):
        """
        Returns the value that would violate the fewest constraints when assigned to a variable.

        Args:
            variable (str): The name of the variable.

        Returns:
            bool: The least constraining value for the variable.
        """

        domain = self.variables[var]
        # Storing each value and its associated constraint violation count
        violations = []

        for value in domain:
            violation_count = 0
            for constraint_function, variables in self.var_constraints.get(var, []):
                self.assign(var, value)
                if not self.is_constraint_satisfied((constraint_function, variables)):
                    violation_count += 1
                self.unassign(var)

            violations.append((value, violation_count))

        sorted_values = [value for value, _ in sorted(
            violations, key=lambda x: x[1])]

        return sorted_values
