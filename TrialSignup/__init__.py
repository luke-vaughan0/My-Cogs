from .TrialSignup import TrialSignup


def setup(bot):
    bot.add_cog(TrialSignup(bot))
