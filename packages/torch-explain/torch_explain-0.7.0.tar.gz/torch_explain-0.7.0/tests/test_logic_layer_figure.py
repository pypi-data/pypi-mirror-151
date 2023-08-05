import torch
import torch.nn.functional as F
import torch_explain as te
from torch_explain.logic.nn.entropy import explain_class

y_pred, y = torch.FloatTensor(), torch.FloatTensor()
x_train, y_train, x_val, y_val = torch.FloatTensor(), torch.FloatTensor()

e_len = torch.nn.Sequential(
    te.nn.EntropyLinear(20, 10, n_classes=2),
    torch.nn.LeakyReLU(),
    torch.nn.Linear(10, 1),
)

loss = F.binary_cross_entropy(y_pred, y_train) + te.nn.functional.entropy_logic_loss(e_len)

logic_explanation = explain_class(e_len, x_train, y_train, x_val, y_val, target_class=1)


        optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
        loss_form = torch.nn.BCEWithLogitsLoss()
        model.train()

        concept_names = ['x1', 'x2', 'x3', 'x4']
        target_class_names = ['y', '¬y', 'z', '¬z']

        for epoch in range(7001):
            # train step
            optimizer.zero_grad()
            y_pred = model(x).squeeze(-1)
            loss = loss_form(y_pred, y) + 0.0001 * te.nn.functional.entropy_logic_loss(model)
            loss.backward()
            optimizer.step()

            # compute accuracy
            if epoch % 100 == 0:
                accuracy = (y_pred>0.5).eq(y).sum().item() / (y.size(0) * y.size(1))
                print(f'Epoch {epoch}: loss {loss:.4f} train accuracy: {accuracy:.4f}')

                # extract logic formulas
                for target_class in range(y.shape[1]):
                    explanation_class_i, exp_raw = entropy.explain_class(model, x, y1h, x, y1h, target_class,
                                                                         concept_names=concept_names)
                    accuracy_i, preds = test_explanation(exp_raw, x, y1h, target_class)
                    if explanation_class_i: explanation_class_i = explanation_class_i.replace('&', '∧').replace('|', '∨').replace('~', '¬')
                    explanation_class_i = f'∀x: {explanation_class_i} ↔ {target_class_names[target_class]}'

                    print(f'\tExplanation class {target_class} (acc. {accuracy_i*100:.2f}): {explanation_class_i}')
                    print()

        return


if __name__ == '__main__':
    unittest.main()
