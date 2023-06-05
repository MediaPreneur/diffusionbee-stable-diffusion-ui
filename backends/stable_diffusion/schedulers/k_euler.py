import numpy as np


def get_alphas_cumprod(beta_start=0.00085, beta_end=0.0120, n_training_steps=1000):
    betas = np.linspace(beta_start ** 0.5, beta_end ** 0.5, n_training_steps, dtype=np.float32) ** 2
    alphas = 1.0 - betas
    return np.cumprod(alphas, axis=0)



class KEulerSampler():
    def __init__(self, n_inference_steps=50, n_training_steps=1000):
        pass

    def set_timesteps(self, n_inference_steps, n_training_steps=1000): #dg
        timesteps = np.linspace(n_training_steps - 1, 0, n_inference_steps)

        alphas_cumprod = get_alphas_cumprod(n_training_steps=n_training_steps)
        sigmas = ((1 - alphas_cumprod) / alphas_cumprod) ** 0.5
        log_sigmas = np.log(sigmas)
        log_sigmas = np.interp(timesteps, range(n_training_steps), log_sigmas)
        sigmas = np.exp(log_sigmas)
        sigmas = np.append(sigmas, 0)
        
        self.sigmas = sigmas
        self.initial_scale = sigmas.max()
        self.timesteps = timesteps
        self.n_inference_steps = n_inference_steps
        self.n_training_steps = n_training_steps
        self.step_count = 0


    def get_input_scale(self, step_count=None):
        if step_count is None:
            step_count = self.step_count
        sigma = self.sigmas[step_count]
        return 1 / (sigma ** 2 + 1) ** 0.5

    def add_noise(self, latent, noise, idx ): #dg
        for i in idx:
            assert idx[0] == i
        sc = self.sigmas[idx[0]]
        return latent + noise*sc


    def step(self, output , t , latents , seed=None ): #dg
       

        sigma_from = self.sigmas[t]
        sigma_to = self.sigmas[t + 1]
        latents += output * (sigma_to - sigma_from)
        return {"prev_sample": latents } #latents