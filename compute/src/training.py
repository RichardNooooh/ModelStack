import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch import jit
import torch.optim as optim

from jobs import Job, JobStatus

from tqdm import tqdm

# TODO generalize
# TODO clean and refactor
def load_data():
    train_loader = DataLoader(datasets.MNIST('/storage/datasets/', 
                                            download=False, 
                                            train=True,
                                            transform=transforms.ToTensor()),
                                batch_size=10, 
                                shuffle=True)
    test_loader = DataLoader(datasets.MNIST('/storage/datasets/', 
                                            download=False, 
                                            train=False,
                                            transform=transforms.ToTensor()),
                                batch_size=10, 
                                shuffle=True)
    return train_loader, test_loader

def load_model(model_path):
    return jit.load(model_path)


def train(model, criterion, optimizer, num_epochs, train_loader, test_loader):
    model.train()
    for epoch in range(num_epochs):
        for images, labels in train_loader:
            # images, labels = images.to(device), labels.float().unsqueeze(1).to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        
        print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}')
        evaluate(model, test_loader)

def evaluate(model, test_loader):
    model.eval()  # Set the model to evaluation mode
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            # images, labels = images.to(device), labels.float().unsqueeze(1).to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    print(f'Test Accuracy: {accuracy}%\n')
    model.train()

def begin_training(job: Job):
    model = load_model(job.model_path)
    job.updateStatus(JobStatus.RUNNING)

    train_loader, test_loader = load_data()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=job.lr)

    evaluate(model, test_loader)
    train(model, criterion, optimizer, job.num_epochs, train_loader, test_loader)
    # evaluate(model, test_loader)

    model.eval()
    jit.save(model, job.model_path)

    print("finished job.")
    job.updateStatus(JobStatus.DONE)

