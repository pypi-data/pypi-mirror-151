import torch.nn as nn
import torchvision.models as models

from NaroNet.Patch_Contrastive_Learning.exceptions.exceptions import InvalidBackboneError


class ResNetSimCLR_pretrained(nn.Module):

    def __init__(self, in_channels, base_model, out_dim):
        super(ResNetSimCLR_pretrained, self).__init__()
        self.resnet_dict = {"resnet50": models.resnet50(pretrained=True)}#, num_classes=out_dim)}

        self.backbone = self._get_basemodel(base_model)        

        self.backbone.conv1 = nn.Conv2d(in_channels, self.backbone.conv1.out_channels, self.backbone.conv1.kernel_size, 
                                        stride=self.backbone.conv1.stride, padding=self.backbone.conv1.padding)

        # add mlp projection head
        #self.backbone.fc = nn.Sequential(nn.Linear(out_dim, 1028), nn.ReLU(), nn.Linear(1000, out_dim), nn.ReLU(), self.backbone.fc)
        self.backbone.fc = nn.Sequential(self.backbone.fc,nn.ReLU(),nn.Linear(1000, out_dim),nn.ReLU() ,nn.Linear(out_dim, 1028))

    def _get_basemodel(self, model_name):
        try:
            model = self.resnet_dict[model_name]
        except KeyError:
            raise InvalidBackboneError(
                "Invalid backbone architecture. Check the config file and pass one of: resnet18 or resnet50")
        else:
            return model

    def forward(self, x):
        return self.backbone(x)



class ResNetSimCLR(nn.Module):

    def __init__(self, in_channels, base_model, out_dim):
        super(ResNetSimCLR, self).__init__()
        self.resnet_dict = {"resnet18": models.resnet18(pretrained=False, num_classes=out_dim),
                            "resnet50": models.resnet50(pretrained=False, num_classes=out_dim)}

        self.backbone = self._get_basemodel(base_model)
        dim_mlp = self.backbone.fc.in_features

        self.backbone.conv1 = nn.Conv2d(in_channels, self.backbone.conv1.out_channels, self.backbone.conv1.kernel_size, 
                                        stride=self.backbone.conv1.stride, padding=self.backbone.conv1.padding)

        # add mlp projection head
        self.backbone.fc = nn.Sequential(nn.Linear(dim_mlp, dim_mlp), nn.ReLU(), self.backbone.fc)

    def _get_basemodel(self, model_name):
        try:
            model = self.resnet_dict[model_name]
        except KeyError:
            raise InvalidBackboneError(
                "Invalid backbone architecture. Check the config file and pass one of: resnet18 or resnet50")
        else:
            return model

    def forward(self, x):
        return self.backbone(x)

